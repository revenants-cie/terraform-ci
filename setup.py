"""Setup module"""
from textwrap import dedent
from setuptools import setup, find_packages


def parse_requirements(req_file):
    """
    Parse file with requirements and return a dictionary
    consumable by setuptools.

    :param req_file: path to requirements file.
    :type req_file: str
    :return: Dictionary with requirements.
    :rtype: dict
    """
    with open(req_file) as fdescr:
        reqs = fdescr.read().strip().split("\n")
    return [x for x in reqs if x and not x.strip().startswith("#")]


REQUIREMENTS = parse_requirements("requirements/requirements.txt")
TEST_REQUIREMENTS = parse_requirements("requirements/requirements_test.txt")
SETUP_REQUIREMENTS = parse_requirements("requirements/requirements_setup.txt")

if __name__ == "__main__":
    setup(
        name="terraform-ci",
        version="1.0.0",
        description="Terraform CI runs terraform in Travis-CI",
        long_description=dedent(
            """
            Terraform CI runs "terraform plan, "terraform apply"
            and publishes the plan output to GitHub pull request.
            """
        ),
        author="TwinDB",
        author_email="dev@twindb.com",
        url="https://github.com/twindb/terraform-ci",
        packages=find_packages(exclude=("tests*",)),
        package_dir={"terraform_ci": "terraform_ci"},
        entry_points={
            "console_scripts": [
                "install-terraform=terraform_ci.install_terraform:main",
                "terraform-ci=terraform_ci.ci_runner:terraform_ci",
            ]
        },
        include_package_data=True,
        install_requires=REQUIREMENTS,
        license="Apache Software License 2.0",
        zip_safe=False,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Natural Language :: English",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
        ],
        setup_requires=SETUP_REQUIREMENTS,
        test_suite="tests",
        tests_require=TEST_REQUIREMENTS,
        python_requires=">=3.6",
    )
