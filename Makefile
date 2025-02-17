### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

# Python checks
PYTHON?=python3

# installed?
ifeq (, $(shell which $(PYTHON) ))
  $(error "PYTHON=$(PYTHON) not found in $(PATH)")
endif

# version ok?
PYTHON_VERSION_MIN=3.10
PYTHON_VERSION_OK=$(shell $(PYTHON) -c "import sys; print((int(sys.version_info[0]), int(sys.version_info[1])) >= tuple(map(int, '$(PYTHON_VERSION_MIN)'.split('.'))))")
ifeq ($(PYTHON_VERSION_OK),0)
  $(error "Need python $(PYTHON_VERSION) >= $(PYTHON_VERSION_MIN)")
endif

BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

GIT_FOLDER=$(BACKEND_FOLDER)/.git
VENV_FOLDER=$(BACKEND_FOLDER)/.venv
BIN_FOLDER=$(VENV_FOLDER)/bin


all: help

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

$(BIN_FOLDER)/pip $(BIN_FOLDER)/tox $(BIN_FOLDER)/pipx $(BIN_FOLDER)/uv $(BIN_FOLDER)/mxdev:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	$(PYTHON) -m venv $(VENV_FOLDER)
	$(BIN_FOLDER)/pip install -U "pip" "uv" "wheel" "pipx" "tox" "pre-commit"
	if [ -d $(GIT_FOLDER) ]; then $(BIN_FOLDER)/pre-commit install; else echo "$(RED) Not installing pre-commit$(RESET)";fi

.PHONY: check
check: $(BIN_FOLDER)/tox ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	$(BIN_FOLDER)/tox -e lint

.PHONY: test
test: $(BIN_FOLDER)/tox ## Run tests
	$(BIN_FOLDER)/tox -e test

.PHONY: livehtml
livehtml: $(BIN_FOLDER)/tox ## Build docs and watch for changes
	@echo "$(GREEN)==> Building docs$(RESET)"
	$(BIN_FOLDER)/tox -e livehtml

.PHONY: linkcheck
linkcheck: $(BIN_FOLDER)/tox ## Check links in documentation
	@echo "$(GREEN)==> Checking links in documentation$(RESET)"
	$(BIN_FOLDER)/tox -e linkcheck

.PHONY: clean
clean: ## Clean environment
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	rm -rf $(VENV_FOLDER) pyvenv.cfg .tox .venv _build

