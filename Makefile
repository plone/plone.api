# convenience makefile to boostrap & run buildout

version = 2.7
python = python$(version)
options =

all: docs tests

docs: docs/html/index.html

docs/html/index.html: docs/*.rst src/plone/api/*.py bin/sphinx-build
	bin/sphinx-build docs docs/html

bin/sphinx-build: .installed.cfg

.installed.cfg: bin/buildout buildout.cfg
	bin/buildout $(options)

bin/buildout: buildout.cfg bootstrap.py
	$(python) bootstrap.py -d
	@touch bin/buildout

tests: .installed.cfg
	@bin/test

clean:
	-rm -rf .installed.cfg bin docs/html parts develop-eggs

.PHONY: all docs tests clean

