"""Helper functions to run terraform in CI or workstation."""
import json
import logging
import sys
from contextlib import contextmanager
from glob import glob
from os import environ, path as osp
from shutil import copy2, rmtree
from subprocess import Popen, PIPE, CalledProcessError
from tempfile import mkdtemp
from urllib.parse import urlparse

import boto3
import hcl

__version__ = "0.9.0"

DEFAULT_TERRAFORM_VARS = ".env/tf_env.json"
LOG = logging.getLogger(__name__)


class LessThanFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    """Filters out log messages of a lower level."""

    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        # non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0


def render_comment(status):
    """
    Format status with markdown syntax to publish it as a comment.

    :param status: Status generated by a series of terraform plan.
        For example::

        {'cloudflare': {'add': 0,
                        'change': 0,
                        'destroy': 0,
                        'stderr': b'',
                        'success': True},
         'github': {'add': 0,
                    'change': 0,
                    'destroy': 0,
                    'stderr': b'',
                    'success': True},
         'management_app': {'add': 0,
                            'change': 0,
                            'destroy': 0,
                            'stderr': b'',
                            'success': True},
         'prod/recovery_app': {'add': 0,
                               'change': 0,
                               'destroy': 0,
                               'stderr': b'',
                               'success': True},
         'prod/web_app': {'add': 0,
                          'change': 0,
                          'destroy': 0,
                          'stderr': b'',
                          'success': True},
         'stage/recovery_app2': {'add': 0,
                                 'change': 0,
                                 'destroy': 0,
                                 'stderr': b'',
                                 'success': True},
         'stage/web_app': {'add': 0,
                           'change': 0,
                           'destroy': 0,
                           'stderr': b'',
                           'success': True}}
    :type status: dict
    :return: Markdown formatted comment
    :rtype: str
    """
    print(status)
    # 1/0
    map_change = {
        "add": "![#c5f015](https://placehold.it/15/c5f015/000000?text=+) ",
        "change": "![#1589F0](https://placehold.it/15/1589F0/000000?text=+) ",
        "destroy": "![#f03c15](https://placehold.it/15/f03c15/000000?text=+) ",
        None: "![#FFFF00](https://placehold.it/15/FFFF00/000000?text=+) ",
    }

    def flag(local_change):
        for k in status.keys():
            try:
                if status[k][local_change] > 0:
                    return map_change[local_change]
            except TypeError:
                return map_change[None]

        return ""

    comment = " | ".join(
        [
            "Module",
            "Success",
            flag("add") + "Add",
            flag("change") + "Change",
            flag("destroy") + "Destroy",
        ]
    )
    comment += "\n" + "--- | --- | ---: | ---: | ---:" + "\n"

    tag_map = {
        True: "![#c5f015](https://placehold.it/15/c5f015/000000?text=+)",
        False: "![#f03c15](https://placehold.it/15/f03c15/000000?text=+)",
    }
    for key in status.keys():
        changes = {}
        for change in ["add", "change", "destroy"]:
            try:
                if status[key][change] > 0:
                    changes[change] = "**%d**" % status[key][change]
                else:
                    changes[change] = status[key][change]
            except TypeError:
                changes[change] = "Unknown"

        line = "**{module}** | {tag} `{success}` " "| {add} | {change} | {destroy}"
        line = line.format(
            module=key,
            tag=tag_map[status[key]["success"]],
            success=status[key]["success"],
            add=changes["add"],
            change=changes["change"],
            destroy=changes["destroy"],
        )
        comment += line + "\n"
    for key in status.keys():
        outs = {}
        for out in ["stdout", "stderr"]:
            if isinstance(status[key][out], bytes):
                outs[out] = status[key][out].decode("utf-8")
            else:
                outs[out] = status[key][out]

        line = """
# **{module}**

## stdout

{cout}

## stderr

{cerr}
"""
        line = line.format(
            module=key,
            cout="```" + outs["stdout"] + "```" if outs["stdout"] else "_no output_",
            cerr="```" + outs["stderr"] + "```" if outs["stderr"] else "_no output_",
        )
        comment += line

    return comment


def get_action(branch=None, pull_request=False):
    """
    Detect terraform action based on input branch and pull_request flag.
    If it cannot detect the action (branch is not given or error) the action
    will be ``plan``.

    :param branch: Branch name.
    :type branch: str
    :param pull_request: Whether the branch is a pull request.
    :type pull_request: bool
    :return: "apply" or "plan". It will return "apply" only if the branch is
        "master" and not a pull request.
    :rtype: str
    """
    if branch == "master" and not pull_request:
        return "apply"

    return "plan"


def parse_plan(output):
    """
    Parse a string given by output and return a tuple with execution plan.

    :param output: Output of terraform plan command.
    :type output: str
    :return: Tuple with number of changes (add, change, destroy)
    :rtype: tuple
    """
    add = None
    change = None
    destroy = None
    try:
        for line in output.splitlines():
            if line.startswith("Plan: "):
                split_line = line.split()
                # Plan: 4 to add, 11 to change, 7 to destroy.
                add = int(split_line[1])
                change = int(split_line[4])
                destroy = int(split_line[7])
            elif line == "No changes. Infrastructure is up-to-date.":
                return 0, 0, 0

    except AttributeError:
        pass

    return add, change, destroy


def run_job(path, action):
    """
    Run a job for a given module specified by path.

    :param path: Path to terraform module.
    :type path: str
    :param action: "apply" or "plan". Other action are not supported.
    :return: Dictionary with run report:

        {
            'success': True or False
            'add': x,
            'change': x,
            'destroy': x,
            'raw': <original content of the plan output>
        }
    :rtype: dict
    """
    returncode, cout, cerr = execute(["make", "-C", path, action])
    status = {"success": returncode == 0, "stderr": cerr, "stdout": cout}
    parse_tree = parse_plan(cout.decode("utf-8"))
    status["add"] = parse_tree[0]
    status["change"] = parse_tree[1]
    status["destroy"] = parse_tree[2]

    return status


def execute(cmd, stdout=PIPE, stderr=PIPE, cwd=None):
    """
    Execute a command and return a tuple with return code, STDOUT and STDERR.

    :param cmd: Command.
    :type cmd: list
    :param stdout: Where to send stdout. Default PIPE.
    :type stdout: int, None
    :param stderr: Where to send stdout. Default PIPE.
    :type stderr: int, None
    :param cwd: Working directory.
    :type cwd: str
    :return: Tuple (return code, STDOUT, STDERR)
    :rtype: tuple
    """
    LOG.info("Executing: %s", " ".join(cmd))
    proc = Popen(cmd, stdout=stdout, stderr=stderr, cwd=cwd)
    cout, cerr = proc.communicate()
    return proc.returncode, cout, cerr


def read_from_secretsmanager(url):
    """
    Read a secret from AWS secrets manager.

    ``url`` is where the secret value is stored and has format:

        secretsmanager://<secret name>:<json key>

    "secret name" is the secret identifier as AWS calls it in Secrets Manager.
    It is assumed the secret stores a JSON string. The function returns
    value of the "json key".

    :param url: URL to a secret value.
    :type url: str
    :return: Secret value that is stored in a JSON key "json key".
    :rtype: str
    """
    client = boto3.client("secretsmanager")
    location = urlparse(url)
    full_path = location.netloc + location.path
    aws_response = client.get_secret_value(SecretId=full_path.split(":")[0])
    try:
        return json.loads(aws_response["SecretString"])[full_path.split(":")[1]]

    except json.JSONDecodeError:
        return aws_response["SecretString"]


def setup_environment(config_path=DEFAULT_TERRAFORM_VARS):
    """
    Read AWS variables from Terraform config and set them
    as environment variables
    """
    with open(config_path) as f_descr:
        tf_vars = json.loads(f_descr.read())

    var_map = {
        "TF_VAR_aws_access_key": ["AWS_ACCESS_KEY_ID", "TF_VAR_aws_access_key_id"],
        "TF_VAR_aws_secret_key": [
            "AWS_SECRET_ACCESS_KEY",
            "TF_VAR_aws_secret_access_key",
        ],
    }
    for key in var_map:
        try:
            for eq_key in var_map[key]:
                environ[eq_key] = tf_vars[key]

        except KeyError:
            pass

    for variable in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]:
        try:
            environ[variable] = tf_vars["TF_VAR_{var}".format(var=variable.lower())]

        except KeyError as err:
            LOG.debug("Key %s is missing in %s", err, config_path)

    for key, value in tf_vars.items():
        if value.startswith("secretsmanager://"):
            environ[key] = read_from_secretsmanager(value)
        else:
            environ[key] = value

    for variable in ["GITHUB_TOKEN"]:
        try:
            environ[variable] = environ["TF_VAR_{var}".format(var=variable.lower())]

        except KeyError as err:
            LOG.debug("Key %s is missing in %s", err, config_path)


def module_name_from_path(path):
    """
    Get one level up directory and return it as module name

    :param path: Path to directory
    :return: parent directory
    :rtype: str
    """
    abspath = osp.abspath(path)

    if abspath == "/":
        return "root"

    return osp.basename(abspath)


def convert_to_newlines(text):
    """
    Convert \n in the bytes ``text`` into actual new lines.

    :param text: Input string where new lines are encoded as ``\n``
    :type text: bytes
    :return: Text where \n are replaced with actual new lines.
    :rtype: str
    """
    return text.replace(b"\\n", b"\n").decode("UTF-8")


def setup_logging(logger, debug=False):  # pragma: no cover
    """Configures logging for the module"""

    fmt_str = (
        "%(asctime)s: %(levelname)s:"
        " %(module)s.%(funcName)s():%(lineno)d: %(message)s"
    )

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.addFilter(LessThanFilter(logging.WARNING))
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(fmt_str))

    # Log errors and warnings to stderr
    console_handler_err = logging.StreamHandler(stream=sys.stderr)
    console_handler_err.setLevel(logging.WARNING)
    console_handler_err.setFormatter(logging.Formatter(fmt_str))

    # Log debug to stderr
    console_handler_debug = logging.StreamHandler(stream=sys.stderr)
    console_handler_debug.addFilter(LessThanFilter(logging.INFO))
    console_handler_debug.setLevel(logging.DEBUG)
    console_handler_debug.setFormatter(logging.Formatter(fmt_str))

    logger.handlers = []
    logger.addHandler(console_handler)
    logger.addHandler(console_handler_err)

    if debug:
        logger.addHandler(console_handler_debug)
        logger.debug_enabled = True

    logger.setLevel(logging.DEBUG)


def terraform_output(path):
    """
    Run terraform output and return the json results as a dict.

    :param path: Path to directory with terraform module.
    :type path: str
    :return: dict from terraform output
    :rtype: dict
    """
    cmd = "terraform output -json"
    ret, cout, cerr = execute(cmd.split(), stdout=PIPE, stderr=None, cwd=path)
    if ret:
        raise CalledProcessError(returncode=ret, cmd=cmd, output=cout, stderr=cerr)
    return json.loads(cout)


@contextmanager
def terraform_apply(
    path,  # pylint: disable=bad-continuation
    destroy_after=True,  # pylint: disable=bad-continuation
    json_output=False,  # pylint: disable=bad-continuation
    var_file="configuration.tfvars",  # pylint: disable=bad-continuation
):
    """
    Run terraform init and apply, then return a generator.
    If destroy_after is True, run terraform destroy afterwards.

    :param path: Path to directory with terraform module.
    :type path: str
    :param destroy_after: Run terraform destroy after context it returned back.
    :type destroy_after: bool
    :param json_output: Yield terraform output result as a dict (available in the context)
    :type json_output: bool
    :param var_file: Path to a file with terraform variables.
    :type var_file: str
    :return: If json_output is true then yield the result from terraform_output otherwise nothing.
        Use it in the ``with`` block.
    :raise CalledProcessError: if either of terraform commands (except ``terraform destroy``)
        exits with non-zero.
    """
    cmds = [
        "terraform init -no-color",
        "terraform get -update=true -no-color",
        (
            "terraform apply -var-file={var_file} -input=false "
            "-auto-approve".format(var_file=var_file)
        ),
    ]
    try:
        for cmd in cmds:
            ret, cout, cerr = execute(cmd.split(), stdout=None, stderr=None, cwd=path)
            if ret:
                raise CalledProcessError(
                    returncode=ret, cmd=cmd, output=cout, stderr=cerr
                )
        if json_output:
            yield terraform_output(path)
        else:
            yield

    finally:
        if destroy_after:
            execute(
                "terraform destroy -var-file={var_file} "
                "-input=false -auto-approve".format(var_file=var_file).split(),
                stdout=None,
                stderr=None,
                cwd=path,
            )


@contextmanager
def strip_backend(path):
    """
    Copy terraform file (found by a suffix ``*.tf``) to a temporary directory.
    While copying look for backend configuration and skip it.
    This is needed to prepare module code for a unit test. In the production module
    you may want to configure state to save in an S3 bucket, but for a test it's not needed,
    the state is temporary.

    The function returns path to the temporary directory.

    After the function exits the ``with`` scope the temporary directory will be removed.

    :param path: path to terraform module.
    :type path: str
    :return: Path to temporary directory with the original terraform files except
        one with the backend configuration.
    :rtype: str
    """
    tmpdir = mkdtemp()

    def copy_file(src, dst):
        LOG.debug("%s => %s", src, dst)
        copy2(src, dst)

    try:
        for tf_file in glob(osp.join(path, "*.tf")):
            try:
                if "terraform" in hcl.load(open(tf_file)):
                    LOG.debug("Found backend config in %s. Skipping it.", tf_file)
                    continue

                copy_file(tf_file, osp.join(tmpdir, osp.basename(tf_file)))

            except ValueError:
                LOG.warning("Failed to parse %s, will copy it anyway.", tf_file)
                copy_file(tf_file, osp.join(tmpdir, osp.basename(tf_file)))

        yield tmpdir

    finally:
        rmtree(tmpdir)
