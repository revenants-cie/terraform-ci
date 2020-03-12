"""convert_to_newlines() tests"""
import sys

import pytest

from terraform_ci import convert_to_newlines


@pytest.mark.parametrize(
    "input_text, expected",
    [
        (b"hello", "hello"),
        (
            b"terraform init -no-color\n\n",
            """terraform init -no-color

""",
        ),
        (None, ""),
        ("", ""),
    ],
)
def test_convert_to_newlines(input_text, expected, capsys):
    """Check that new lines are printed"""
    sys.stdout.write(convert_to_newlines(input_text))
    captured = capsys.readouterr()
    assert captured.out == expected
    assert captured.err == ""
