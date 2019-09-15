"""Module prepares terraform binary"""
from os import path as osp
from shutil import rmtree
from subprocess import check_call
from tempfile import mkdtemp

from terraform_ci import LOG

TERRAFORM_VERSION = "0.12.7"

TERRAFORM_DISTRIBUTION_URL = "https://releases.hashicorp.com/" \
                             "terraform/{version}/terraform_{version}" \
                             "_linux_amd64.zip"\
    .format(version=TERRAFORM_VERSION)

BINDIR = '/usr/local/bin/'


def install_terraform():
    """Download terraform binary from hashicorp website and
    install it in local binary directory.
    """
    tmpdir = mkdtemp()

    try:
        terraform_file = 'terraform.zip'
        LOG.info('Downloading terraform from %s', TERRAFORM_DISTRIBUTION_URL)
        check_call(
            [
                'wget',
                '--quiet',
                TERRAFORM_DISTRIBUTION_URL,
                '-O', terraform_file
            ],
            cwd=tmpdir
        )

        LOG.info(
            'Extracting %s in %s',
            osp.join(
                tmpdir, terraform_file
            ),
            BINDIR
        )
        check_call(
            [
                'sudo',
                'unzip',
                '-n',           # never overwrite existing files,
                '-q',           # quiet mode
                '-d', BINDIR,   # extract files into exdir
                terraform_file
            ],
            cwd=tmpdir
        )

    finally:
        LOG.info('Cleaning up %s', tmpdir)
        rmtree(tmpdir, ignore_errors=True)


if __name__ == '__main__':
    install_terraform()
