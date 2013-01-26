.. line-block::

    WARNING: If you are reading this on GitHub, DON'T! Read it on ReadTheDocs:
    http://ploneapi.readthedocs.org/en/latest/contribute/conventions.html so you
    have working references and proper formatting.

.. _conventions:

===========
Conventions
===========

We've modeled the following rules and recommendations based on the following
documents:

 * `PEP8 <http://www.python.org/dev/peps/pep-0008>`__
 * `PEP257 <http://www.python.org/dev/peps/pep-0257>`_
 * `Rope project <http://rope.sourceforge.net/overview.html>`_
 * `Google Style Guide <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>`_
 * `Pylons Coding Style <http://docs.pylonsproject.org/en/latest/community/codestyle.html>`_
 * `Tim Pope on Git commit messages <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`__

Line length
===========

All Python code in this package should be PEP8 valid. This includes adhering
to the 80-char line length. If you absolutely need to break this rule, append
``# noPEP8`` to the offending line to skip it in syntax checks.

.. note::
    Configuring your editor to display a line at 79th column helps a lot
    here and saves time.

.. note::
    The line length rule also applies to non-python source files, such as
    documentation .rst files or .zcml files, but is a bit more relaxed there.

Breaking lines
--------------

Based on code we love to look at (Pyramid, Requests, etc.), we allow the
following two styles for breaking long lines into blocks:

1. Break into next line with one additional indent block.

   .. sourcecode:: python

       foo = do_something(
           very_long_argument='foo', another_very_long_argument='bar')

       # For functions the ): needs to be placed on the following line
       def some_func(
           very_long_argument='foo', another_very_long_argument='bar'
       ):

2. If this still doesn't fit the 80-char limit, break into multiple lines.

   .. sourcecode:: python

       foo = dict(
           very_long_argument='foo',
           another_very_long_argument='bar',
       )

       a_long_list = [
           "a_fairly_long_string",
           "quite_a_long_string_indeed",
           "an_exceptionally_long_string_of_characters",
       ]

 * Arguments on first line, directly after the opening parenthesis are
   forbidden when breaking lines.
 * The last argument line needs to have a trailing comma (to be nice to the
   next developer coming in to add something as an argument and minimize VCS
   diffs in these cases).
 * The closing parenthesis or bracket needs to have the same indentation level
   as the first line.
 * Each line can only contain a single argument.
 * The same style applies to dicts, lists, return calls, etc.

This package follows all rules above, `check out the source
<https://github.com/plone/plone.api/tree/master/src/plone/api>`_ to see them
in action.


Docstrings style
================

Read and follow http://www.python.org/dev/peps/pep-0257/. There is one
exception though: We reject BDFL's recommendation about inserting a blank line
between the last paragraph in a multi-line docstring and its closing quotes as
it's Emacs specific and two emacs users here on the Beer & Wine Sprint both
support our way.

If you wanna be extra nice, you are encouraged to document your method's
parameters and their return values in a `reST field list syntax
<http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists>`_.

.. sourcecode:: rest


    :param foo: blah blah
    :type foo: string
    :param bar: blah blah
    :type bar: int
    :returns: something

Check out the `plone.api source
<https://github.com/plone/plone.api/tree/master/src/plone/api>`_ for more
usage examples.


Unit tests style
================

Read http://www.voidspace.org.uk/python/articles/unittest2.shtml to learn what
is new in unittest2 and use it.

This is not true for in-line documentation tests. Those still use old unittest
test-cases, so you cannot use ``assertIn`` and similar.


String formatting
=================

As per http://docs.python.org/2/library/stdtypes.html#str.format, we should
prefer the new style string formatting (``.format()``) over the old one
(``% ()``).


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

    from plone.app.testing import something
    from zope.component import getMultiAdapter
    from zope.component import getSiteManager

instead of

.. sourcecode:: python

    from plone.app.testing import *
    from zope.component import getMultiAdapter, getSiteManager

4. Don't catch ImportError to detect whether a package is available or not.
   Instead, use pkg_resources.get_distribution and catch DistributionNotFound.

.. sourcecode:: python

    import pkg_resources

    try:
        pkg_resources.get_distribution('plone.dexterity')
    except pkg_resources.DistributionNotFound:
        HAS_DEXTERITY = False
    else:
        HAS_DEXTERITY = True

instead of

.. sourcecode:: python

    try:
        import plone.dexterity
        HAVE_DEXTERITY = True
    except ImportError:
        HAVE_DEXTERITY = False

Grouping and sorting
--------------------

Since Plone has such a huge code base, we don't want to loose developer time
figuring out into which group some import goes (standard lib?, external
package?, etc.). So we just sort everything alphabetically and insert one blank
line between `from foo import bar` and `import baz` blocks. Conditional imports
come last. Again, we *do not* distinguish between what is standard lib,
external package or internal package in order to save time and avoid the hassle
of explaining which is which.

.. sourcecode:: python

    from __future__ import division
    from Acquisition import aq_inner
    from plone.api import portal
    from plone.api.exc import MissingParameterError
    from Products.CMFCore.interfaces import ISiteRoot
    from Products.CMFCore.WorkflowCore import WorkflowException

    import pkg_resources
    import random

    try:
        pkg_resources.get_distribution('plone.dexterity')
    except pkg_resources.DistributionNotFound:
        HAS_DEXTERITY = False
    else:
        HAS_DEXTERITY = True


Declaring dependencies
======================

All direct dependencies should be declared in ``install_requires`` or
``extras_require`` sections in setup.py. Dependencies, which are not needed for
a production environment (like "develop" or "test" dependencies) or are
optional (like "archetypes" or "dexterity" flavors of the same package) should
go in ``extras_require``. Remember to document how to enable specific features
(and think of using ``zcml:condition`` statements, if you have such optional
features).

Generally all direct dependencies (packages directly imported or used in ZCML)
should be declared, even if they would already be pulled in by other
dependencies. This explicitness reduces possible runtime errors and gives a
good overview on the complexity of a package.

For example, if you depend on ``Products.CMFPlone`` and use ``getToolByName``
from ``Products.CMFCore``, you should also declare the ``CMFCore`` dependency
explicitly, even though it's pulled in by Plone itself. If you use namespace
packages from the Zope distribution like ``Products.Five`` you should
explicitly declare ``Zope`` as dependency.

Inside each group of dependencies, lines should be sorted alphabetically.


Versioning scheme
=================

For software versions, use a sequence-based versioning scheme:

    MAJOR.MINOR[.MICRO][STATUS]

For more information, read http://semver.org/.


Restructured Text versus Plain Text
===================================

Use the Restructured Text (.rst file extension) format instead of plain text
files (.txt file extension) for all documentation, including doctest files.
This way you get nice syntax highlighting and formating in recent text editors,
on GitHub and with Sphinx.


.. _changes:

Tracking changes
================

Feature-level changes to code are tracked inside ``docs/CHANGES.rst``. Example:

.. sourcecode:: rst

    CHANGES
    =======

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
current development changes block.


.. _sphinx-docs:

Sphinx Documentation
====================

Un-documented code is broken code.

For every feature you add to the codebase you should also add documentation
for it to ``docs/``.

After adding/modifying documentation, run ``make`` to re-generate your docs.

Publicly available documentation on http://api.plone.org is automatically
generated from these source files, periodically. So when you push changes
to master on GitHub you should soon be able to see them published on
api.plone.org.

Read the `reStructuredText Primer <http://sphinx-doc.org/rest.html>`_ to brush
up on your `reST` skills.


.. _travis_ci:

Travis Continuous Integration
=============================

On every push to GitHub, `Travis <http://travis-ci.org/plone/plone.api>`_
runs all tests and syntax validation checks and reports build outcome to
the ``#sprint`` IRC channel and the person who committed the last change.

Travis is configured with the ``.travis.yml`` file located in the root of this
package.


.. _git_workflow:

Git workflow & branching model
==============================

Our repository on GitHub has the following layout:

* **feature branches**: all development for new features must be done in
  dedicated branches, normally one branch per feature,
* **master branch**: when features get completed they are merged into the master
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

Git dotfiles
------------

Plone developers have dotfiles similar to these:
https://github.com/plone/plone.dotfiles.


Git Commit Message Style
------------------------

`Tim Pope's post on Git commit message style <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`__ is widely considered the gold standard:

::

    Capitalized, short (50 chars or less) summary

    More detailed explanatory text, if necessary.  Wrap it to about 72
    characters or so.  In some contexts, the first line is treated as the
    subject of an email and the rest of the text as the body.  The blank
    line separating the summary from the body is critical (unless you omit
    the body entirely); tools like rebase can get confused if you run the
    two together.

    Write your commit message in the imperative: "Fix bug" and not "Fixed bug"
    or "Fixes bug."  This convention matches up with commit messages generated
    by commands like git merge and git revert.

    Further paragraphs come after blank lines.

    - Bullet points are okay, too
    - Typically a hyphen or asterisk is used for the bullet, preceded by a
    single space, with blank lines in between, but conventions vary here
    - Use a hanging indent

`Github flavored markdown  <http://github.github.com/github-flavored-markdown/>`_ is also useful in commit messages.
