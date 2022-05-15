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

# TODO Remove complete Makefile when Netlify build command is switched from 'make netlify' to 'tox -e docs'.

# Just a developer helper. Can be replaced by 'tox -e docs' ('tox -e plone6docs') 
.PHONY: docs-html
docs-html: bin/python bin/pip ## Build documentation
	bin/pip install tox
	bin/tox -e plone6docs
	@echo
	@echo "Build of documentation finished. The HTML pages are in _build/plone6docs/html."

.PHONY: livehtml
livehtml:
	sphinx-autobuild  -b html -d _build/plone6docs/doctrees docs _build/plone6docs/html $(O)

# TODO Remove when Netlify build command is switched from 'make netlify' to 'tox -e docs'.
.PHONY: netlify
netlify: bin/python bin/pip ## Build documentation (Netlfy style)
	bin/pip install tox
	bin/tox -e plone6docs
	@echo
	@echo "Build of documentation finished. The HTML pages are in _build/plone6docs/html."

## Run conversion of documentation from restructuredText to myST
# TODO Remove later when MyST documentation is settled.
.PHONY: conversion-to-myst
conversion-to-myst: bin/python bin/pip
	bin/pip install "rst-to-myst[sphinx]"
	-bin/rst2myst convert -R docs/*.rst
	-bin/rst2myst convert -R docs/**/*.rst
	python fix-converted-myst.py
	make netlify
