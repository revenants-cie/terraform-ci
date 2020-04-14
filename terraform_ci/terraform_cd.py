"""terraform-cd deploys artifacts to S3."""
import sys
from os import environ, path as osp
from subprocess import Popen
from tempfile import TemporaryDirectory

import boto3
import click
from botocore.exceptions import ClientError

from terraform_ci import DEFAULT_TERRAFORM_VARS, setup_environment, LOG, setup_logging


def get_default_module_name():
    """
    Guess terraform module name from environment, current directory, etc.

    :return: Best guess for terraform module name
    :rtype: str
    """
    try:
        return environ["TRAVIS_REPO_SLUG"].split("/")[1]
    except KeyError:
        return osp.basename(osp.abspath(osp.curdir))


@click.command()
@click.version_option()
@click.option("--debug", help="Print debug messages", is_flag=True, default=False)
@click.option(
    "--module-version",
    help="Module version to use. It is supposed to be a git tag "
    "but may be any valid git ref e.g. master, develop, commit id.",
    required=True,
)
@click.option(
    "--module-name",
    default=get_default_module_name(),
    help=(
        "Use this string as module name. By default it's either "
        "repo name if defined in Travis-CI environment "
        "or the current directory name."
    ),
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
@click.argument("bucket")
def terraform_cd(**kwargs):
    """
    Publish Terraform module in S3 bucket.
    """
    module_name = kwargs["module_name"]
    tag = kwargs["module_version"]
    release_archive = "{project}-{tag}.tar.gz".format(project=module_name, tag=tag)
    bucket = kwargs["bucket"]
    setup_logging(LOG, debug=kwargs["debug"])

    with TemporaryDirectory() as tmp_dir:

        with open(osp.join(tmp_dir, release_archive), "wb") as archive_descriptor:
            proc = Popen(
                [
                    "git",
                    "archive",
                    "--format=tar.gz",
                    "--prefix={project}-{tag}/".format(project=module_name, tag=tag),
                    tag,
                ],
                stdout=archive_descriptor,
            )
        proc.communicate()

        setup_environment(
            config_path=kwargs["env_file"], role=kwargs["aws_assume_role_arn"]
        )

        try:
            s3_client = boto3.client("s3")

            with open(osp.join(tmp_dir, release_archive), "rb") as archive_descriptor:
                s3_client.upload_fileobj(
                    archive_descriptor,
                    bucket,
                    osp.join(module_name, release_archive),
                    ExtraArgs={"ACL": "bucket-owner-full-control"},
                )
                LOG.info(
                    "Published artifact to s3://%s/%s",
                    bucket,
                    osp.join(module_name, release_archive),
                )

        except ClientError as err:
            LOG.error(err)
            try:
                sts_client = boto3.client("sts")
                LOG.error("AWS caller: %s", sts_client.get_caller_identity()["Arn"])

            except ClientError:
                LOG.warning(
                    "Failed to get AWS caller. Probably the client is not authenticated."
                )

            sys.exit(1)
