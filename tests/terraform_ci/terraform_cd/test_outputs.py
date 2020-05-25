"""Tests for terraform_cd()."""
import os
from pathlib import Path
from subprocess import run, PIPE

from click.testing import CliRunner
from terraform_ci.terraform_cd import terraform_cd


def test_terraform_cd_outputs():
    """
    Test if --include-artifacts generates the same structure as git archive
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        for directory in ["local", "git", "test"]:
            os.mkdir(directory)

        os.chdir("test")

        for f_name in range(10):
            Path(f"{f_name}.py").touch()

        run("git init", shell=True, check=True)
        run("git add .", shell=True, check=True)
        run("git commit -a -m test1", shell=True, check=True)
        run("git tag 0.1.1", shell=True, check=True)

        result = runner.invoke(
            terraform_cd,
            [
                "--debug",
                "--include-artifacts",
                "--module-name=test",
                "--module-version=0.1.1",
                "--target=local",
                "../local/",
            ],
        )
        assert result.exit_code == 0

        result = runner.invoke(
            terraform_cd,
            [
                "--debug",
                "--module-name=test",
                "--module-version=0.1.1",
                "--target=local",
                "../git/",
            ],
        )
        assert result.exit_code == 0

        os.chdir("..")

        git_out = run(
            "tar -tf ./git/test-0.1.1.tar.gz | sort",
            shell=True,
            check=True,
            stdout=PIPE
        )
        local_out = run(
            "tar -tf ./local/test-0.1.1.tar.gz | sort",
            shell=True,
            check=True,
            stdout=PIPE,
        )
        assert len(git_out.stdout) > 0
        assert git_out.stdout == local_out.stdout


def test_terraform_cd_outputs2():
    """
    Test if build directory is omitted from the git archive
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        for directory in ["local", "git", "test"]:
            os.mkdir(directory)

        os.chdir("test")

        for f_name in range(10):
            Path(f"{f_name}.py").touch()

        run("git init", shell=True, check=True)
        run("git add .", shell=True, check=True)
        run("git commit -a -m test1", shell=True, check=True)
        run("git tag 0.1.1", shell=True, check=True)

        # simulate the build process by creating a dummy build structure
        os.mkdir("build")
        for f_name in range(10):
            Path(f"build{f_name}.artifact").touch()

        result = runner.invoke(
            terraform_cd,
            [
                "--debug",
                "--include-artifacts",
                "--module-name=test",
                "--module-version=0.1.1",
                "--target=local",
                "../local/",
            ],
        )
        assert result.exit_code == 0

        result = runner.invoke(
            terraform_cd,
            [
                "--debug",
                "--module-name=test",
                "--module-version=0.1.1",
                "--target=local",
                "../git/",
            ],
        )
        assert result.exit_code == 0

        os.chdir("..")

        git_out = run(
            "tar -tf ./git/test-0.1.1.tar.gz | sort",
            shell=True,
            check=True,
            stdout=PIPE
        )
        local_out = run(
            "tar -tf ./local/test-0.1.1.tar.gz | sort",
            shell=True,
            check=True,
            stdout=PIPE,
        )

        # git archive shouldn't include the build directory hence the difference
        assert len(git_out.stdout) > 0
        assert len(git_out.stdout) < len(local_out.stdout)
