SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

version = 3

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`


# all: .installed.cfg

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



bin/python bin/pip:
	python$(version) -m venv . || virtualenv --python=python$(version) .
	bin/python -m pip install --upgrade pip


# Documentation
# ----------------------------------------------------------------------

.PHONY: netlify
netlify:
	bin/pip install tox
	tox -e plone6docs
	@echo
	@echo "Build finished. The HTML pages are in _build/plone6docs/html."

