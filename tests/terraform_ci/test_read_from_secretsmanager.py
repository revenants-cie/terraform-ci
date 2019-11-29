"""Tests for read_from_secretsmanager()."""
import mock
import pytest

from terraform_ci import read_from_secretsmanager


@pytest.mark.parametrize('url, key, secret_string', [
    (
        'secretsmanager:///path/to/secret:key',
        '/path/to/secret',
        '{"key": "foo_value"}'
    ),
    (
        'secretsmanager://secret:key',
        'secret',
        '{"key": "foo_value"}'
    ),
    (
        'secretsmanager://secret',
        'secret',
        'foo_value'
    )
])
@mock.patch('terraform_ci.boto3')
def test_read_from_secretsmanager(mock_boto3, url, key, secret_string):
    """Read secret from correct ID"""
    mock_client = mock.Mock()
    mock_boto3.client.return_value = mock_client
    mock_client.get_secret_value.return_value = {
        'ARN': 'string',
        'Name': 'string',
        'VersionId': 'string',
        'SecretString': secret_string,
        'VersionStages': [
            'string',
        ]
    }
    assert read_from_secretsmanager(url) == 'foo_value'
    mock_client.get_secret_value.assert_called_once_with(
        SecretId=key
    )
