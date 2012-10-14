.. line-block::

    WARNING: If you are reading this on GitHub, DON'T! Read it on ReadTheDocs:
    http://ploneapi.readthedocs.org/en/latest/contribute/conventions.html so you
    have working references and proper formatting.

.. _conventions:

===========
Conventions
===========

Line length
===========

All Python code in this package should be PEP8 valid. However, we don't strictly
enforce the 80-char line length rule. It is encouraged to have your code
formatted in 80-char lines, but somewhere it's just more readable to break this
rule for a few characters. Long and descriptive test method names are a good
example of this.

.. note::
    Configuring your editor to display a line at 80th column helps a lot
    here and saves time.

.. note::
    The line length rules also applies to non-python source files, such as
    documentation .rst files.


Docstrings style
================

Read and follow http://www.python.org/dev/peps/pep-0257/. That's it.


About imports
=============

1. Don't use * to import `everything` from a module.
2. Don't use commas to import multiple stuff on a single line.
3. Don't use relative paths.

.. sourcecode:: python

    from zope.component import getMultiAdapter
    from zope.component import getSiteManager

instead of

.. sourcecode:: python

    from plone.app.testing import *
    from zope.component import getMultiAdapter, getSiteManager
    from .portal import get


Sort imports
============

As another imports stylistic guide: Imports of code from other modules should
always be alphabetically sorted with no empty lines between imports. The only
exception to this rule is to keep one empty line between a group of
``from x import y`` and a group of ``import y`` imports.

.. sourcecode:: python

    from App.config import getConfiguration
    from plone.app.testing import login

    import os

instead of

.. sourcecode:: python

    import os

    from plone.app.testing import login
    from App.config import getConfiguration


.. _changelog:

Changelog
=========

Feature-level changes to code are tracked inside ``docs/HISTORY.txt``. Examples:

- added feature X
- removed Y
- fixed bug Z

Add an entry every time you add/remove a feature, fix a bug, etc.


.. _sphinx-docs:

Sphinx Documentation
====================

Un-documented code is broken code.

For every feature you add to the codebase you should also add documentation
for it to ``docs/``.

After adding/modifying documentation, run ``make`` to re-generate your docs.

Also, documentation is automatically generated from these source files every
time code is pushed to `master` branch on GitHub. The post-commit hook is
handled by ReadTheDocs and the results (nice HTML pages) are visible at
http://ploneapi.readthedocs.org/en/latest/.


.. _travis_ci:

Travis Continuous Integration
=============================

On every push to GitHub, `Travis <http://travis-ci.org/plone/plone.api>`_
runs all tests and syntax validation checks and reports build outcome to
``TODO: which?`` mailinglist and to the ``#sprint`` IRC channel.

Travis is configured with the ``.travis.yml`` file located in the root of this
package.


.. _git_workflow:

Git workflow & branching model
==============================

Our repository on GitHub has the following layout:

* **feature branches**: all development for new features must be done in
  dedicated branches, normaly one branch per feature,
* **master branch**: when features get completed they are merged into the maste
  branch; bugfixes are commited directly on the master branch,
* **tags**: whenever we create a new release we tag the repository so we can
  later re-trace our steps, re-release versions, etc.


.. _setting_up_git:

Setting up Git
==============

Git is a very useful tool, especially when you configure it to your needs. Here
are a couple of tips.

Enhanced git prompt
-------------------

Do one (or more) of the following:

* http://clalance.blogspot.com/2011/10/git-bash-prompts-and-tab-completion.html
* http://en.newinstance.it/2010/05/23/git-autocompletion-and-enhanced-bash-prompt/
* http://gitready.com/advanced/2009/02/05/bash-auto-completion.html


Example of ``~/.gitconfig``
---------------------------

.. sourcecode:: ini

    [user]
        name = John Smith
        email = john.smith@gmail.com
    [diff "cfg"]
        funcname = ^\\(\\[.*\\].*\\)$
    [color]
        diff = auto
        status = auto
        branch = auto
    [alias]
        st = status
        ci = commit
        br = branch
        co = checkout
    [core]
        excludesfile = /home/jsmith/.gitignore
        editor = nano
    [github]
        user = jsmith
        token = <token_here>

Example of ``~/.gitignore``
---------------------------

.. sourcecode:: ini

    # Compiled source #
    ###################
    *.com
    *.class
    *.dll
    *.exe
    *.o
    *.so
    *.lo
    *.la
    *.rej
    *.pyc
    *.pyo

    # Packages #
    ############
    # it's better to unpack these files and commit the raw source
    # git has its own built in compression methods
    *.7z
    *.dmg
    *.gz
    *.iso
    *.jar
    *.rar
    *.tar
    *.zip

    # Logs and databases #
    ######################
    *.log
    *.sql
    *.sqlite

    # OS generated files #
    ######################
    .DS_Store
    .DS_Store?
    ehthumbs.db
    Icon?
    Thumbs.db

    # Python projects related #
    ###########################
    *.egg-info
    Makefile
    .egg-info.installed.cfg
    *.pt.py
    *.cpt.py
    *.zpt.py
    *.html.py
    *.egg


