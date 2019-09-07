"""tests for read() method"""
from terraform_ci.sectionless_configparser import SectionLessConfigParser


def test_get(config_file_path):
    """
    Read ini file from config_file_path and make sure no exception is risen
    """
    parser = SectionLessConfigParser()
    parser.read(config_file_path)
    assert parser.get('foo') == 'bar'
    assert parser.get('xyz') == 'abc'
    assert parser.get('aaa') == 'bbb'
