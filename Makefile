
version = 2.6
python = python$(version)
options =

all: .installed.cfg docs/index.html

docs/index.html: src/plone/api/docs/*.rst src/plone/api/*.py
	bin/sphinx-build src/plone/api/docs docs

.installed.cfg: bin/buildout buildout.cfg
	bin/buildout $(options)

bin/buildout: bootstrap.py
	$(python) bootstrap.py -d

tests: .installed.cfg
	@bin/test

clean:
	-rm -rf .installed.cfg bin docs parts develop-eggs

.PHONY: all docs tests clean

