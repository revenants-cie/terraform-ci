"""Tests for delete_outdated_comments()."""
import os

import mock
import pytest

from terraform_ci import delete_outdated_comments


@pytest.mark.parametrize(
    "token, kwargs", [(None, {}), ("foo_token", {"login_or_token": "foo_token"})]
)
@mock.patch("terraform_ci.Github")
def test_delete_outdated_comments_token_from_args(mock_github, token, kwargs):
    """Check if GitHub() is instantiated with correct github token."""

    delete_outdated_comments({}, "foo_repo", 1, github_token=token)
    mock_github.assert_called_once_with(**kwargs)


@mock.patch("terraform_ci.Github")
def test_delete_outdated_comments_token_from_env(mock_github):
    """Check if GitHub() takes the token from environment"""
    assert "GITHUB_TOKEN" not in os.environ
    try:
        os.environ["GITHUB_TOKEN"] = "foo_token"
        delete_outdated_comments({}, "foo_repo", 1)
        mock_github.assert_called_once_with(login_or_token="foo_token")

    finally:
        del os.environ["GITHUB_TOKEN"]


@pytest.mark.parametrize(
    "status, status_in_comment, expected_delete_calls",
    [
        ({}, None, 0),
        ({}, {}, 1),
        ({"foo": "bar"}, {"foo": "bar"}, 1),
        ({"foo": "bar", "bar": "foo"}, {"bar": "foo", "foo": "bar"}, 1),
        ({"foo": "bar"}, {"bar": "foo"}, 0),
    ],
)
@mock.patch("terraform_ci.Github")
@mock.patch("terraform_ci.get_status_from_comment")
def test_delete_outdated_comments(
        mock_get_status_from_comment,
        mock_github,
        status,
        status_in_comment,
        expected_delete_calls,
):
    """Check if delete() is called."""
    assert "GITHUB_TOKEN" not in os.environ

    mock_client = mock.Mock()
    mock_github.return_value = mock_client

    mock_repo = mock.Mock()
    mock_client.get_repo.return_value = mock_repo

    mock_pull = mock.Mock()
    mock_repo.get_pull.return_value = mock_pull

    author = "foo_user"
    mock_comment = mock.Mock()
    mock_comment.user.login = author
    mock_pull.get_issue_comments.return_value = [mock_comment]

    mock_get_status_from_comment.return_value = status_in_comment

    mock_user = mock.Mock()
    mock_user.login = author
    mock_client.get_user.return_value = mock_user

    delete_outdated_comments(status, "foo_repo", 123)

    mock_github.assert_called_once_with()
    mock_client.get_repo.assert_called_once_with("foo_repo")
    mock_client.get_user.assert_called_once_with()
    mock_repo.get_pull.assert_called_once_with(123)
    mock_pull.get_issue_comments.assert_called_once_with()
    assert mock_comment.delete.call_count == expected_delete_calls
