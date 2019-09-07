"""parse_plan() tests."""
# pylint: disable=line-too-long
from textwrap import dedent
import pytest

from terraform_ci import parse_plan


@pytest.mark.parametrize('output, result', [
    (
        "",
        (None, None, None)
    ),
    (
        None,
        (None, None, None)
    ),
    (
        dedent(
            """
            github_repository_webhook.slack: Refreshing state... (ID: 103656263)

            ------------------------------------------------------------------------

            An execution plan has been generated and is shown below.
            Resource actions are indicated with the following symbols:
              ~ update in-place

            Terraform will perform the following actions:

            ~ module.dd-agent-packaging.github_repository.twindb-cie_repo
                  default_branch: "develop" => "master"

              ~ module.twindb-cie-terraform-modules.github_repository.twindb-cie_repo
                  default_branch: "develop" => "master"
            Plan: 4 to add, 11 to change, 7 to destroy.

            ------------------------------------------------------------------------

            Note: You didn't specify an "-out" parameter to save this plan, so Terraform
            can't guarantee that exactly these actions will be performed if
            "terraform apply" is subsequently run.
            """
        ),
        (4, 11, 7)
    ),
    (
        dedent(
            """
            Refreshing Terraform state in-memory prior to plan...
            The refreshed state will be used to calculate this plan, but will not be
            persisted to local or remote state storage.

            aws_s3_bucket.omnibus-cache-twindb-cie-backup: Refreshing state... (ID: omnibus-cache-twindb-cie-backup)
            cloudflare_record.jumphost_record: Refreshing state... (ID: fc27e59c7fcef641f9e39787c924b6b2)

            ------------------------------------------------------------------------

            No changes. Infrastructure is up-to-date.

            This means that Terraform did not detect any differences between your
            configuration and real physical resources that exist. As a result, no
            actions need to be performed.
            """
        ),
        (0, 0, 0)
    )
])
def test_parse_plan(output, result):
    """
    parse_plan() returns valid result.

    :param output: terraform plan output.
    :param result: expected result.
    """
    assert parse_plan(output) == result
