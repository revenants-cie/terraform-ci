.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        print("%-40s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < Makefile

.PHONY: bootstrap
bootstrap: ## bootstrap the development environment
	pip install -U "pip ~= 19.1"
	pip install -U "setuptools ~= 41.0"
	pip install -r requirements/requirements.txt \
		-r requirements/requirements_setup.txt \
		-r requirements/requirements_test.txt
	pip install --editable .

.PHONY: install
install: ## install the package
	python setup.py install

.PHONY: test
test: ## run unit tests
	black --check terraform_ci
	python setup.py test

.PHONY: test-all
test-all: ## run unit tests on all supported python versions
	tox

clean: clean-build clean-pyc clean-test clean-docs ## remove all build, test, coverage and Python artifacts

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -rf pkg/
	rm -rf cache/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

clean-docs:
	rm -rf docs/_build
