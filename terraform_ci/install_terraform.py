"""Module prepares terraform binary"""
import sys

from os import path as osp
from shutil import rmtree
from subprocess import check_call
from tempfile import mkdtemp

import click

from terraform_ci import LOG, setup_logging

DEFAULT_TERRAFORM_VERSION = "0.12.9"
TERRAFORM_DISTRIBUTION_URL = (
    "https://releases.hashicorp.com/"
    "terraform/{version}/terraform_{version}"
    "_linux_amd64.zip"
)
DEFAULT_BINDIR = "/usr/local/bin"


@click.command()
@click.version_option()
@click.option("--debug", help="Show debug messages", is_flag=True, default=False)
@click.option(
    "--terraform-version",
    help="Terraform version to install",
    default=DEFAULT_TERRAFORM_VERSION,
    show_default=True,
)
@click.option(
    "--bin-dir",
    help="Directory where terraform binary will be installed",
    default=DEFAULT_BINDIR,
    show_default=True,
)
def main(debug, terraform_version, bin_dir):
    """
    Install terraform binary locally.
    """
    setup_logging(LOG, debug=debug)
    install_terraform(terraform_version, bindir=bin_dir)


def install_terraform(version=DEFAULT_TERRAFORM_VERSION, bindir=DEFAULT_BINDIR):
    """Download terraform binary from hashicorp website and
    install it in local binary directory.

    :param version: Terraform version
    :type version: str
    :param bindir: Directory to install terraform
    :type bindir: str
    """
    assert sys.platform == "linux", "This must be run on Linux 64 bit only"
    tmpdir = mkdtemp()

    try:
        terraform_file = "terraform.zip"
        LOG.info(
            "Downloading terraform from %s",
            TERRAFORM_DISTRIBUTION_URL.format(version=version),
        )
        check_call(
            [
                "wget",
                "--quiet",
                TERRAFORM_DISTRIBUTION_URL.format(version=version),
                "-O",
                terraform_file,
            ],
            cwd=tmpdir,
        )

        LOG.info("Extracting %s in %s", osp.join(tmpdir, terraform_file), bindir)
        check_call(
            [
                "sudo",
                "unzip",
                "-n",  # never overwrite existing files,
                "-q",  # quiet mode
                "-d",
                bindir,  # extract files into exdir
                terraform_file,
            ],
            cwd=tmpdir,
        )

    finally:
        LOG.info("Cleaning up %s", tmpdir)
        rmtree(tmpdir, ignore_errors=True)
