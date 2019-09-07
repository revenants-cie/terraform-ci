"""parse_requirements() tests."""
from textwrap import dedent

import pytest

from setup import parse_requirements


@pytest.mark.parametrize('req_content, expected', [
    (
        dedent(
            """
            urllib3>=1.23,<2.0
            dnspython>=1.15.0,<2.0.0
            requests>=2.19.1,<3.0.0
            srvlookup>=1.0.0,<2.0.0
            hvac>=0.6.3,<1.0.0
            """
        ),
        [
            'urllib3>=1.23,<2.0',
            'dnspython>=1.15.0,<2.0.0',
            'requests>=2.19.1,<3.0.0',
            'srvlookup>=1.0.0,<2.0.0',
            'hvac>=0.6.3,<1.0.0'
        ]
    ),
    (
        dedent(
            """
            mock
            pytest>=2.9.0
            pytest-sugar
            pytest-timeout
            pytest-xdist
            bumpversion

            pylint < 1.8.1
            pytest-cov
            pycodestyle

            # Sphinx dependencies conflict with others
              # As a workaround the versions are pinned
            Sphinx
            """
        ),
        [
            'mock',
            'pytest>=2.9.0',
            'pytest-sugar',
            'pytest-timeout',
            'pytest-xdist',
            'bumpversion',
            'pylint < 1.8.1',
            'pytest-cov',
            'pycodestyle',
            'Sphinx'
        ]
    )
])
def test_parse_requirements(req_content, expected, tmpdir):
    """Check that the function returns valid dictionary."""
    reqs_file = tmpdir.join('reqs.txt')
    reqs_file.write(req_content)

    assert parse_requirements(str(reqs_file)) == expected
