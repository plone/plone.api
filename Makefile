
version = 2.6
python = python$(version)
options =

all: .installed.cfg docs/index.html

docs/index.html: src/plone/api/docs/*.rst
	bin/sphinx-build src/plone/api/docs docs

.installed.cfg: buildout.cfg
	bin/buildout $(options)

bin/buildout: buildout.cfg bootstrap.py
	$(python) bootstrap.py -d

clean:
	-rm -rf .installed.cfg bin docs parts develop-eggs

.PHONY: all docs clean

