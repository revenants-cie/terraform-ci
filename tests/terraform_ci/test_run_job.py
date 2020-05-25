"""run_job() tests"""
# pylint: disable=line-too-long
# noinspection PyPackageRequirements
import mock

from terraform_ci import run_job


@mock.patch("terraform_ci.execute")
def test_run_job_apply(mock_execute):
    """
    Test that run_job() returns a valid status on successful terraform plan.
    """
    mock_execute.return_value = 0, None, None
    status = run_job("foo", "bar")
    assert status["add"] is None
    assert status["change"] is None
    assert status["destroy"] is None
