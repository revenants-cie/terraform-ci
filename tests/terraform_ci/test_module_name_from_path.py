"""
Tests for module_name_from_path()
"""
import pytest

from terraform_ci import module_name_from_path


@pytest.mark.parametrize('path, module_name', [
    (
        '/foo/bar/',
        'bar'
    ),
    (
        '/',
        'root'
    )
])
def test_module_name_from_path(path, module_name):
    """
    Get module name from path.

    If we are in /foo/bar/ directory the module name will be bar.
    If we are in the root directory - '/' - then the function should
    return the 'root' string.
    """
    assert module_name_from_path(path) == module_name


def test_module_name_from_path_from_cur_dir(tmpdir):
    """
    Get module name from current directory
    """
    path = tmpdir.mkdir('foo')
    assert module_name_from_path(path) == 'foo'
