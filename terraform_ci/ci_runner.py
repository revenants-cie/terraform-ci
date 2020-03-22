"""Module runs a job in Travis-CI."""
import sys
from os import environ, path as osp, EX_SOFTWARE
import click

from terraform_ci import (
    DEFAULT_TERRAFORM_VARS,
    setup_environment,
    run_job,
    render_comment,
    module_name_from_path,
    convert_to_newlines,
    setup_logging,
    LOG,
    delete_outdated_comments,
    terraform_output,
)
from terraform_ci.post_plan import post_comment


@click.command()
@click.version_option()
@click.option("--debug", help="Print debug messages", is_flag=True, default=False)
@click.option(
    "--modules-path",
    default="./",
    help="Path to directory with Terraform modules",
    show_default=True,
)
@click.option(
    "--module-name",
    default=None,
    help="Use this string as module name",
    show_default=True,
)
@click.option(
    "--env-file",
    help="A JSON file with terraform environment variables",
    default=DEFAULT_TERRAFORM_VARS,
    show_default=True,
)
@click.option(
    "--aws-assume-role-arn",
    help="ARN of any role the environment should assume to setup environment.",
    default="",
    show_default=False,
    required=False,
)
@click.argument("action", type=click.Choice(["plan", "apply", "destroy"]))
def terraform_ci(**kwargs):
    """
    Run Terraform action.

    The tool prepares environment, sets environment variables for
    API keys, passwords, roles etc.

    It then runs a terraform action which may be either plan or apply.

    ci-runner can be called in a CI environment or locally on
    a workstation.
    """
    debug = kwargs["debug"]
    modules_path = kwargs["modules_path"]
    module_name = kwargs["module_name"]
    env_file = kwargs["env_file"]
    aws_assume_role_arn = kwargs["aws_assume_role_arn"]
    action = kwargs["action"]

    setup_logging(LOG, debug=debug)

    try:
        pull_request = not environ["TRAVIS_PULL_REQUEST"] == "false"

    except KeyError:
        pull_request = False

    try:
        setup_environment(env_file, role=aws_assume_role_arn)

    except FileNotFoundError:
        LOG.warning("Environment file %s doesn't exit", env_file)

    # module name is parent directory
    mod = module_name or module_name_from_path(modules_path)
    LOG.info("Processing module %s", mod)

    status = {mod: run_job(osp.join(modules_path), action)}
    outputs = terraform_output(osp.join(modules_path))
    if "github_token" in outputs:
        LOG.info(
            "Setting GITHUB_TOKEN and TF_VAR_github_token environment variable from module outputs."
        )
        environ["GITHUB_TOKEN"] = outputs["github_token"]["value"]
        environ["TF_VAR_github_token"] = outputs["github_token"]["value"]

    if status[mod]["success"]:
        LOG.info("%s success: %s", mod, status[mod]["success"])
    else:
        LOG.error("Failed to process %s", mod)
        LOG.error("STDOUT: %s", status[mod]["stdout"].decode("utf-8"))
        LOG.error("STDERR: %s", status[mod]["stderr"].decode("utf-8"))
        sys.exit(EX_SOFTWARE)

    if pull_request:
        delete_outdated_comments(
            status, environ["TRAVIS_REPO_SLUG"], int(environ["TRAVIS_PULL_REQUEST"])
        )
        post_comment(comment=render_comment(status))
    else:
        LOG.info("Standard output:")
        sys.stdout.write(convert_to_newlines(status[mod]["stdout"]) or "no output\n")
        LOG.info("Standard error output:")
        sys.stderr.write(convert_to_newlines(status[mod]["stderr"]) or "no output\n")
