# convenience makefile to boostrap & run buildout
# use `make options=-v` to run buildout with extra options

version = 2.7
python = bin/python$(version)
options =

all: docs tests

docs: docs/html/index.html

docs/html/index.html: docs/*.rst src/plone/api/*.py bin/sphinx-build
	bin/sphinx-build docs docs/html

bin/sphinx-build: .installed.cfg

.installed.cfg: bin/buildout buildout.cfg
	bin/buildout $(options)

bin/buildout: $(python) buildout.cfg bootstrap.py
	$(python) bootstrap.py -d
	@touch $@

$(python):
	virtualenv-$(version) --no-site-packages .
	@touch $@

tests: .installed.cfg
	@bin/test

clean:
	@rm -rf .installed.cfg bin docs/html parts develop-eggs \
		src/plone.api.egg-info lib include .Python

.PHONY: all docs tests clean

