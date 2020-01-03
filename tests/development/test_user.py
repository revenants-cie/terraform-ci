"""Development tests."""
import os

from github import Github


def test_auth_user():
    """Find current user."""
    github_client = Github(os.environ["GITHUB_TOKEN"])
    print(github_client.get_user().login)
