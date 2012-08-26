Update translations
===================

$ cd docs
$ make gettext
$ msgfmt -c -vv --statistics "locale/es/LC_MESSAGES/about.po" -o "translated/es/LC_MESSAGES/about.mo"

Build localized documentation
=============================

#. change ``language`` in conf.py to your language
#. run bin/sphinxbuilder
#. your docs are in docs/html
