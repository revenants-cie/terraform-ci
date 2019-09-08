"""Tests for setup_environment()"""
from os import environ

from terraform_ci import setup_environment


def test_setup_environment(tmpdir):
    """Make sure setup_environment() sets all given variables"""
    conf = tmpdir.join('foo.json')
    conf.write(
        """
        {
            "TF_VAR_aws_access_key_id": "foo",
            "TF_VAR_aws_secret_access_key": "bar",
            "SOME_FOOBAR": "foobar"
        }
        """
    )

    setup_environment(config_path=str(conf))
    assert environ["TF_VAR_aws_access_key_id"] == "foo"
    assert environ["TF_VAR_aws_secret_access_key"] == "bar"
    assert environ["SOME_FOOBAR"] == "foobar"
    # make sure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY are also set
    assert environ["AWS_ACCESS_KEY_ID"] == "foo"
    assert environ["AWS_SECRET_ACCESS_KEY"] == "bar"


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


def test_setup_environment_old_aws_key_name(tmpdir):
    """
    Treat AWS_ACCESS_KEY_ID and AWS_ACCESS_KEY same way.
    """
    conf = tmpdir.join('foo.json')
    conf.write(
        """
        {
            "TF_VAR_aws_access_key": "foo"
        }
        """
    )
    # unset variables
    for variable in ["TF_VAR_aws_access_key_id", "AWS_ACCESS_KEY_ID"]:
        try:
            del environ[variable]

        except KeyError:
            pass

    setup_environment(config_path=str(conf))
    assert environ["TF_VAR_aws_access_key_id"] == "foo"
    assert environ["AWS_ACCESS_KEY_ID"] == "foo"


def test_setup_environment_old_aws_secret_key(tmpdir):
    """
    TF_VAR_aws_secret_key sets AWS_SECRET_ACCESS_KEY as well.
    """
    conf = tmpdir.join('foo.json')
    conf.write(
        """
        {
            "TF_VAR_aws_secret_key": "foo"
        }
        """
    )
    # unset variables
    for variable in ["TF_VAR_aws_secret_access_key", "AWS_SECRET_ACCESS_KEY"]:
        try:
            del environ[variable]

        except KeyError:
            pass

    setup_environment(config_path=str(conf))
    assert environ["TF_VAR_aws_secret_access_key"] == "foo"
    assert environ["AWS_SECRET_ACCESS_KEY"] == "foo"
