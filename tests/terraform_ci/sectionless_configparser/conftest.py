"""Fixtures for SectionLessConfigParser() tests"""
from textwrap import dedent

import pytest


@pytest.fixture
def config_file_path(tmpdir):
    """Returns a string path to a sectionless config"""
    cfg_file = tmpdir.join('conf.ini')
    with open(str(cfg_file), 'w') as fdesc:
        fdesc.write(
            dedent(
                """
                foo = bar
                xyz = "abc"
                aaa = 'bbb'
                """
            )
        )
    return str(cfg_file)
