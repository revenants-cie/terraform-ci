"""Tests for setup_environment()"""
from os import environ

from terraform_ci import setup_environment


def test_setup_environment(tmpdir):
    """Make sure setup_environment() sets all given variables"""
    conf = tmpdir.join('foo.json')
    conf.write(
        """
        {
            "TF_VAR_aws_access_key": "foo",
            "TF_VAR_aws_secret_key": "bar",
            "SOME_FOOBAR": "foobar"
        }
        """
    )

    setup_environment(config_path=str(conf))
    assert environ["TF_VAR_aws_access_key"] == "foo"
    assert environ["TF_VAR_aws_secret_key"] == "bar"
    assert environ["SOME_FOOBAR"] == "foobar"


def test_setup_environment_empty(tmpdir):
    """Make sure setup_environment() doesn't crash"""
    conf = tmpdir.join('foo.json')
    conf.write(
        """
        {
        }
        """
    )

    setup_environment(config_path=str(conf))
