# convenience makefile to boostrap & run buildout
# use `make options=-v` to run buildout with extra options

version = 2.7
python = bin/python
pep8_ignores = E501
options =

all: docs tests

docs: docs/html/index.html

docs/html/index.html: docs/*.rst docs/contribute/*.rst docs/api/*.rst src/plone/api/*.py bin/sphinx-build
	bin/sphinx-build docs docs/html
	@touch $@
	@echo "Documentation was generated at '$@'."

bin/sphinx-build: .installed.cfg
	@touch $@

.installed.cfg: bin/buildout buildout.cfg setup.py
	bin/buildout $(options)

bin/buildout: $(python) buildout.cfg bootstrap.py
	$(python) bootstrap.py -d
	@touch $@

$(python):
	virtualenv-$(version) --no-site-packages .
	@touch $@

tests: .installed.cfg
	@bin/test
	@bin/pyflakes src/
	@bin/pep8 --ignore=$(pep8_ignores) src/

clean:
	@rm -rf .installed.cfg bin docs/html parts develop-eggs \
		src/plone.api.egg-info lib include .Python

.PHONY: all docs tests clean

