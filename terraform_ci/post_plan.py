"""Module for publishing comments to GitHub"""
import json
import os

# noinspection PyPackageRequirements
import sys

from requests import HTTPError, post

from terraform_ci import LOG


def post_comment(comment=None):
    """
    Sends a comment to the pull request as described in
    https://damien.pobel.fr/post/github-api-from-travisci/

    ::

        curl -H "Authorization: token ${GITHUB_TOKEN}" -X POST \
            -d "{\"body\": \"Hello world\"}" \
            "https://api.github.com/repos/${TRAVIS_REPO_SLUG}/
            issues/${TRAVIS_PULL_REQUEST}/comments"
    """
    if comment is None:
        try:
            content = os.environ["COMMENT_CONTENT"]

        except KeyError:
            content = "Empty comment"
    else:
        content = comment

    try:
        pull_request = os.environ["TRAVIS_PULL_REQUEST"]
        if pull_request != "false":
            url = (
                "https://api.github.com/repos/"
                "{TRAVIS_REPO_SLUG}/issues/{TRAVIS_PULL_REQUEST}/comments".format(
                    TRAVIS_REPO_SLUG=os.environ["TRAVIS_REPO_SLUG"],
                    TRAVIS_PULL_REQUEST=pull_request,
                )
            )

            response = post(
                url,
                data=json.dumps({"body": content}),
                headers={
                    "Authorization": "token {github_token}".format(
                        github_token=os.environ["GITHUB_TOKEN"]
                    )
                },
            )
            response.raise_for_status()
            LOG.info("Successfully posted a comment.")
        else:
            LOG.info("Not a pull request - not posting a comment.")

    except KeyError as err:
        LOG.error("Cannot post a comment: %s", content)
        LOG.error("Environment variable %s isn't defined", err)
        sys.exit(1)

    except HTTPError as err:
        LOG.error(err)
        LOG.error(err.response.content)
        sys.exit(1)


if __name__ == "__main__":
    post_comment()
