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

1. Don't use * to import `everything` from a module, because if you do,
   pyflakes cannot detect undefined names (W404).
2. Don't use commas to import multiple stuff on a single line. Some developers
   use IDEs (like `Eclipse <http://pydev.org/>_) or tools (such as `mr.igor
   <http://pypi.python.org/pypi/mr.igor>`_) that expect one import per line.
   Let's be nice to them.
3. Don't use relative paths, again to be nice to people using certain IDEs and
   tools. Also `Google Python Style Guide` recommends against it.

.. sourcecode:: python

    from zope.component import getMultiAdapter
    from zope.component import getSiteManager

instead of

.. sourcecode:: python

    from plone.app.testing import *
    from zope.component import getMultiAdapter, getSiteManager
    from .portal import get


Grouping and sorting
--------------------

Imports should be grouped according to the
`PEP8 <http://www.python.org/dev/peps/pep-0008/#imports>`_ and `rope
<http://rope.sourceforge.net/overview.html#sorting-imports>`_ conventions::

    [__future__ imports]
    from __future__ import division

    [standard imports]
    import random

    [third-party imports]
    from Acquisition import aq_inner
    from Products.CMFCore.interfaces import ISiteRoot
    from Products.CMFCore.WorkflowCore import WorkflowException

    [package imports]
    from plone.api import portal
    from plone.api.exc import MissingParameterError

Inside each group, lines should be alphabetically sorted.


Versioning scheme
=================

For software versions, use a sequence-based versioning scheme:

MAJOR.MINOR[.MICRO][STATUS]

E.g.: 1.2 or 1.2.1

Development releases get a status identifier appended to it.

For the current development branch, just append "dev": 1.3dev. If you make a
development release, append a development status identifier to it. For alpha
releases append a1..an to it, like: 1.3a1. For Beta releases use b1..bn: 1.3b4.
For release canditates use rc1..rcn: 1.3rc2.


Restructured Text versus Plain Text
===================================

User the Restructured Text (.rst file extension) format instead of plain text
files (.txt file extension) for all documentation, including doctest files.
This way you get nice syntax highlighting and formating in recent text editors,
on GitHub and with Sphinx.


.. _changelog:

Changelog
=========

Feature-level changes to code are tracked inside ``CHANGES.rst``. Examples:

.. sourcecode:: rst

    Changelog
    =========

    1.0dev (unreleased)
    -------------------

    - Added feature Z.
      [github_userid1]

    - Removed Y.
      [github_userid2]


    1.0a1 (2012-12-12)
    ------------------

    - Fixed Bug X.
      [github_userid1]


Add an entry every time you add/remove a feature, fix a bug, etc. on top of the
current development changelog block.


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


