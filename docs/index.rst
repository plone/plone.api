.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T! Read it on api.plone.org:
    http://developer.plone.org/reference_manuals/external/plone.api/index.html so you have working
    references and proper formatting.

===========
A Plone API
===========

.. include:: ../README.rst
*******************************

.. topic:: Overview

    The :mod:`plone.api` is an elegant and simple API, built for humans wishing
    to develop with Plone.

    It comes with *cookbook*-like documentation and step-by-step instructions
    for doing common development tasks in Plone. Recipes try to assume the user
    does not have extensive knowledge about Plone internals.

The intention of this package is to provide clear API methods for Plone
functionality which may be confusing or difficult to access. As the underlying
code improves, some API methods may be deprecated, but the documentation
provided here can still be useful.

Some parts of the documentation do not use *plone.api* methods directly, but
simply provide guidance on achieving a task using Plone's internal API. For
example, using the catalog in :ref:`content_find_example`.

The intention is to cover 20% of the tasks any Plone developer does 80% of the
time. By keeping everything in one place, the API stays introspectable and
discoverable, important aspects of being Pythonic.

.. note::

    This package is stable and used in production, but from time to time
    changes will be made to the API. Additional api methods may be introduced
    in minor versions (1.1 -> 1.2). Backward-incompatible changes to the API
    will be restricted to major versions (1.x -> 2.x).


Narrative documentation
=======================

.. toctree::
    :maxdepth: 2

    about.rst
    portal.rst
    content.rst
    user.rst
    group.rst
    env.rst


Complete API and advanced usage
===============================

.. toctree::
    :maxdepth: 1

    api/index.rst
    api/portal.rst
    api/content.rst
    api/user.rst
    api/group.rst
    api/env.rst
    api/exceptions.rst


Contribute
==========

.. toctree::
    :maxdepth: 2

    contribute/index.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
