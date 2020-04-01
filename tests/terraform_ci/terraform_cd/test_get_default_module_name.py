"""Tests for et_default_module_name()."""
from os import environ

from terraform_ci.terraform_cd import get_default_module_name


def test_get_default_module_name_from_env():
    """
    The function can guess project name from travis-ci environment.
    """
    try:
        travis_repo_slug = environ["TRAVIS_REPO_SLUG"]
    except KeyError:
        travis_repo_slug = None

    try:
        environ["TRAVIS_REPO_SLUG"] = "owner_name/repo_name"
        assert get_default_module_name() == "repo_name"
    finally:
        if travis_repo_slug is None:
            del environ["TRAVIS_REPO_SLUG"]
        else:
            environ["TRAVIS_REPO_SLUG"] = travis_repo_slug


def test_get_default_module_name_from_directory():
    """
    The function can guess project name from travis-ci environment.
    """
    assert get_default_module_name() == "terraform-ci"
