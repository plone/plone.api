.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T! Read the documentation
    at `api.plone.org <http://api.plone.org/contribute/conventions.html>`_
    so you have working references and proper formatting.

.. _conventions:

===========
Conventions
===========

.. contents:: :local:

Introduction
==============

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
    documentation ``.rst`` files or ``.zcml`` files,
    but is a bit more relaxed there.

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


Indentation
===========

For Python files, we stick with the `PEP 8 recommondation
<http://www.python.org/dev/peps/pep-0008/#indentation>`_: Use 4 spaces per
indentation level.

For ZCML and XML (GenericSetup) files, we recommend the `Zope Toolkit's coding
style on ZCML <http://docs.zope.org/zopetoolkit/codingstyle/zcml-style.html>`_
::

  Indentation of 2 characters to show nesting, 4 characters to list attributes
  on separate lines. This distinction makes it easier to see the difference
  between attributes and nested elements.


EditorConfig
------------

`EditorConfig <http://editorconfig.org/>`_
provides a way to share the same configuration for all major source code editors.

You only need to install the plugin for your editor of choice,
and add the following configuration on ``~/.editorconfig``.

.. sourcecode:: ini

    [*]
    indent_style = space
    end_of_line = lf
    insert_final_newline = true
    trim_trailing_whitespace = true
    charset = utf-8

    [{*.py,*.cfg}]
    indent_size = 4

    [{*.html,*.dtml,*.pt,*.zpt,*.xml,*.zcml,*.js}]
    indent_size = 2

    [Makefile]
    indent_style = tab

Quoting
=======

For strings and such prefer using single quotes over double quotes. The reason
is that sometimes you do need to write a bit of HTML in your python code, and
HTML feels more natural with double quotes so you wrap HTML string into single
quotes. And if you are using single quotes for this reason, then be consistent
and use them everywhere.

There are two exceptions to this rule:

* docstrings should always use double quotes (as per PEP-257).
* if you want to use single quotes in your string, double quotes might make
  more sense so you don't have to escape those single quotes.

.. sourcecode:: python

    # GOOD
    print 'short'
    print 'A longer string, but still using single quotes.'

    # BAD
    print "short"
    print "A long string."

    # EXCEPTIONS
    print "I want to use a 'single quote' in my string."
    """This is a docstring."""


Docstrings style
================

Read and follow http://www.python.org/dev/peps/pep-0257/. There is one
exception though: We reject BDFL's recommendation about inserting a blank line
between the last paragraph in a multi-line docstring and its closing quotes as
it's Emacs specific and two Emacs users here on the Beer & Wine Sprint both
support our way.

The content of the docstring must be written in the active first-person form,
e.g. "Calculate X from Y" or "Determine the exact foo of bar".

.. sourcecode:: python

    def foo():
        """Single line docstring."""

    def bar():
        """Multi-line docstring.

        With the additional lines indented with the beginning quote and a
        newline preceding the ending quote.
        """

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
usage examples. Also, see the following for examples on how to write
good *Sphinxy* docstrings: http://stackoverflow.com/questions/4547849/good-examples-of-python-docstrings-for-sphinx.



Unit tests style
================

Read http://www.voidspace.org.uk/python/articles/unittest2.shtml to learn what
is new in :mod:`unittest2` and use it.

This is not true for in-line documentation tests. Those still use old unittest
test-cases, so you cannot use ``assertIn`` and similar.


String formatting
=================

As per http://docs.python.org/2/library/stdtypes.html#str.format, we should
prefer the new style string formatting (``.format()``) over the old one
(``% ()``).

Also use numbering, like so:

.. sourcecode:: python

    # GOOD
    print "{0} is not {1}".format(1, 2)


and *not* like this:

.. sourcecode:: python

    # BAD
    print "{} is not {}".format(1, 2)
    print "%s is not %s" % (1, 2)


because Python 2.6 supports only explicitly numbered placeholders.


About imports
=============

1. Don't use ``*`` to import *everything* from a module, because if you do,
   pyflakes cannot detect undefined names (W404).
2. Don't use commas to import multiple things on a single line.
   Some developers use IDEs (like `Eclipse <http://pydev.org/>`_) or tools
   (such as `mr.igor <http://pypi.python.org/pypi/mr.igor>`_)
   that expect one import per line.
   Let's be nice to them.
3. Don't use relative paths, again to be nice to people using certain IDEs and
   tools. Also `Google Python Style Guide` recommends against it.

   .. sourcecode:: python

       # GOOD
       from plone.app.testing import something
       from zope.component import getMultiAdapter
       from zope.component import getSiteManager

   instead of

   .. sourcecode:: python

       # BAD
       from plone.app.testing import *
       from zope.component import getMultiAdapter, getSiteManager

4. Don't catch ``ImportError`` to detect whether a package is available or not,
   as it might hide circular import errors. Instead, use
   ``pkg_resources.get_distribution`` and catch ``DistributionNotFound``. More
   background at http://do3.cc/blog/2010/08/20/do-not-catch-import-errors,-use-pkg_resources/.

   .. sourcecode:: python

       # GOOD
       import pkg_resources

       try:
           pkg_resources.get_distribution('plone.dexterity')
       except pkg_resources.DistributionNotFound:
           HAS_DEXTERITY = False
       else:
           HAS_DEXTERITY = True

   instead of

   .. sourcecode:: python

       # BAD
       try:
           import plone.dexterity
           HAVE_DEXTERITY = True
       except ImportError:
           HAVE_DEXTERITY = False


Grouping and sorting
--------------------

Since Plone has such a huge code base, we don't want to lose developer time
figuring out into which group some import goes (standard lib?, external
package?, etc.). So we just sort everything alphabetically and insert one blank
line between ``from foo import bar`` and ``import baz`` blocks. Conditional imports
come last. Again, we *do not* distinguish between what is standard lib,
external package or internal package in order to save time and avoid the hassle
of explaining which is which.

As for sorting, it is recommended to use case-sensitive sorting. This means
uppercase characters come first, so "Products.*" goes before "plone.*".

.. sourcecode:: python

    # GOOD
    from __future__ import division
    from Acquisition import aq_inner
    from Products.CMFCore.interfaces import ISiteRoot
    from Products.CMFCore.WorkflowCore import WorkflowException
    from plone.api import portal
    from plone.api.exc import MissingParameterError

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
``extras_require`` sections in ``setup.py``. Dependencies, which are not needed for
a production environment (like "develop" or "test" dependencies) or are
optional (like "Archetypes" or "Dexterity" flavors of the same package) should
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

For software versions, use a sequence-based versioning scheme, which is
`compatible with setuptools <http://pythonhosted.org/setuptools/setuptools.html#specifying-your-project-s-version>`_::

    MAJOR.MINOR[.MICRO][STATUS]

The way, setuptools interprets versions is intuitive::

    1.0 < 1.1dev < 1.1a1 < 1.1a2 < 1.1b < 1.1rc1 < 1.1 < 1.1.1

You can test it with setuptools::

    >>> from pkg_resources import parse_version
    >>> parse_version('1.0') < parse_version('1.1.dev')
    ... < parse_version('1.1.a1') < parse_version('1.1.a2')
    ... < parse_version('1.1.b') < parse_version('1.1.rc1')
    ... < parse_version('1.1') < parse_version('1.1.1')

Setuptools recommends to seperate parts with a dot. The website about `semantic
versioning <http://semver.org/>`_ is also worth a read.


Restructured Text versus Plain Text
===================================

Use the Restructured Text (``.rst`` file extension) format instead of plain text
files (``.txt`` file extension) for all documentation, including doctest files.
This way you get nice syntax highlighting and formating in recent text editors,
on GitHub and with Sphinx.


.. _changes:

Tracking changes
================

Feature-level changes to code are tracked inside ``CHANGES.rst``. The title
of the ``CHANGES.rst`` file should be ``Changelog``. Example:

.. sourcecode:: rst

    Changelog
    =========

    1.0.0-dev (Unreleased)
    ----------------------

    - Added feature Z.
      [github_userid1]

    - Removed Y.
      [github_userid2]


    1.0.0-alpha.1 (2012-12-12)
    --------------------------

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
``api.plone.org``.

Read the `reStructuredText Primer <http://sphinx-doc.org/rest.html>`_ to brush
up on your `reST` skills.

Example:

.. sourcecode:: python

    def add(a, b):
        """Calculate the sum of the two parameters.

        Also see the :func:`mod.path.my_func`, :meth:`mod.path.MyClass.method`
        and :attr:`mod.path.MY_CONSTANT` for more details.

        :param a: The first operand.
        :type a: :class:`mod.path.A`

        :param b: The second operand.
        :type b: :class:`mod.path.B`

        :rtype: int
        :return: The sum of the operands.
        :raise: `KeyError`, if the operands are not the correct type.
        """

Attributes are documented using the `#:` marker above the attribute. The
documentation may span multiple lines.

.. sourcecode:: python

    #: Description of the constant value
    MY_CONSTANT = 0xc0ffee

    class Foobar(object):

        #: Description of the class variable which spans over
        #: multiple lines
        FOO = 1


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
* **master branch**: when features get completed they are merged into the
  master branch; bugfixes are commited directly on the master branch,
* **tags**: whenever we create a new release we tag the repository so we can
  later re-trace our steps, re-release versions, etc.


Release process for Plone packages
====================================

To keep the Plone software stack maintainable, the Python egg release process
must be automated to high degree. This happens by enforcing Python packaging
best practices and then making automated releases using the
`zest.releaser <https://github.com/zestsoftware/zest.releaser/>`_  tool.

* Anyone with necessary PyPi permissions must be able to make a new release
  by running the ``fullrelease`` command

... which includes ...

* All releases must be hosted on PyPi

* All versions must be tagged at version control

* Each package must have README.rst with links to the version control
  repository and issue tracker

* CHANGES.txt (docs/HISTORY.txt in some packages) must be always up-to-date and
  must contain list of functional changes which may affect package users.

* CHANGES.txt must contain release dates

* README.rst and CHANGES.txt must be visible on PyPi

* Released eggs must contain generated gettext .mo files, but these files must
  not be committed to the repository (files can be created with
  *zest.pocompile* addon)

* ``.gitignore`` and ``MANIFEST.in`` must reflect the files going to egg (must
  include page template, po files)

More information

* `High quality automated package releases for Python with zest.releaser
  <http://opensourcehacker.com/2012/08/14/high-quality-automated-package-releases-for-python-with-zest-releaser/>`_.


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

`Tim Pope's post on Git commit message style
<http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`__
is widely considered the gold standard:

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

`Github flavored markdown
<http://github.github.com/github-flavored-markdown/>`_
is also useful in commit messages.
