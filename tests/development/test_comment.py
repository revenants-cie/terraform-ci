"""Development tests."""
import os

from github import Github


def test_list_comments():
    """List and delete comments."""
    github_client = Github(os.environ["GITHUB_TOKEN"])
    repo = github_client.get_repo("revenants-cie/terraform-aws-website")
    pull = repo.get_pull(2)
    for comment in pull.get_issue_comments():
        author = comment.user.login
        comment_id = comment.id
        print("Author = %s" % author)
        print("Comment id %d" % comment_id)
        if author == "akuzminsky":
            comment.delete()
