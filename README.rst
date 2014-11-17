plone.api
=========

.. topic:: Overview

    The ``plone.api`` is an elegant and simple API, built for humans wishing to develop with Plone.

    It comes with *cookbook*-like documentation and step-by-step instructions for doing common development tasks in Plone.
    Recipes try to assume the user does not have extensive knowledge about Plone internals.

The intention of this package is to provide clear API methods for Plone functionality which may be confusing or difficult to access.
As the underlying code improves some API methods may be deprecated and the documentation here will be updated to show how to use the improved code (even if it means not using ``plone.api``)

Some parts of the documentation do not use *plone.api* methods directly, but simply provide guidance on achieving a task using Plone's internal API. For example, using the portal catalog (see 'Find content objects').

The intention is to cover 20% of the tasks any Plone developer does 80% of the time.
By keeping everything in one place, the API stays introspectable and discoverable, important aspects of being Pythonic.

.. note::

    This package is stable and used in production, but from time to time changes will be made to the API.
    Additional api methods may be introduced in minor versions (1.1 -> 1.2).
    Backward-incompatible changes to the API will be restricted to major versions (1.x -> 2.x).

Documentation
=============

The full `plone.api documentation <http://docs.plone.org/external/plone.api/docs/contribute/index.html>`_ contains narrative and API documentation.


Source Code
===========

* Contributors please read the document `Process for Plone core's development <http://docs.plone.org/develop/plone-coredev/index.html>`_.
  Also consult the section about contribution in the `plone.api contributors documentation <http://docs.plone.org/external/plone.api/docs/contribute/index.html>`_.

* Sources are at the `Plone code repository hosted at Github <https://github.com/plone/plone.api>`_.

* Please file any `Issues at GitHub <http://github.com/plone/plone.api/issues>`_

* `Continuous Integration is executed using Travis CI <http://travis-ci.org/plone/plone.api>`_.

* `Code Coverage is measured at Coveralls.io <http://coveralls.io/r/plone/plone.api>`_.

