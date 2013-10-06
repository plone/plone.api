***********
A Plone API
***********

.. topic:: Overview

    The ``plone.api`` is an elegant and simple API, built for humans wishing
    to develop with Plone.

    It comes with *cookbook*-like documentation and step-by-step instructions
    for doing common development tasks in Plone. Recipes try to assume the user
    does not have extensive knowledge about Plone internals.

.. raw:: html

    <img src="http://travis-ci.org/plone/plone.api.png?&branch=master">
    <img src="http://coveralls.io/repos/plone/plone.api/badge.png">

* `Documentation @ api.plone.org <http://api.plone.org>`_
* `Source code @ GitHub <http://github.com/plone/plone.api>`_
* `Issues @ GitHub <http://github.com/plone/plone.api/issues>`_
* `Continuous Integration @ Travis CI <http://travis-ci.org/plone/plone.api>`_
* `Code Coverage @ Coveralls.io <http://coveralls.io/r/plone/plone.api>`_

The intention of this package is to be transitional. It points out the parts of
Plone which are particularly nasty -- we hope they will get fixed so that we
can deprecate the ``plone.api`` methods that cover them up, but the
documentation can still be useful.

Some parts of the documentation already are this way: they don't use
``plone.api`` methods directly, but simply provide guidance on achieving a task
using Plone's internals. Example: usage of the catalog in `Find content`
example.

The intention is to cover 20% of the tasks we do 80% of the time. Keeping
everything in one place helps keep the API introspectable and discoverable,
which are important aspects of being Pythonic.

.. note::

    This package is still under development, but should be fairly stable and is
    already being used in production. It's currently a release candidate,
    meaning that we don't intend to change method signatures, but it may still
    happen.

