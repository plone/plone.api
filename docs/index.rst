.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T!
    Read the documentation at `docs.plone.org <http://docs.plone.org/develop/plone.api/docs/index.html>`_
    so you have working references and proper formatting.

===========
A Plone API
===========

    The ``plone.api`` is an elegant and simple API, built for humans wishing to develop with Plone.

    It comes with *cookbook*-like documentation and step-by-step instructions for doing common development tasks in Plone.
    Recipes try to assume the user does not have extensive knowledge about Plone internals.

The intention of this package is to provide clear API methods for Plone functionality which may be confusing or difficult to access.
As the underlying code improves, some API methods may be deprecated and the documentation
here will be updated to show how to use the improved code (even if it means not using ``plone.api``).

Some parts of the documentation do not use *plone.api* methods directly, but simply provide guidance on achieving
a task using Plone's internal API.

For example, using the portal catalog (see 'Find content objects').

The intention is to cover 20% of the tasks any Plone developer does 80% of the time.
By keeping everything in one place, the API stays introspectable and discoverable, important aspects of being Pythonic.

.. note::

    This package is stable and used in production, but from time to time changes will be made to the API.
    Additional API methods may be introduced in minor versions (1.1 -> 1.2).
    Backward-incompatible changes to the API will be restricted to major versions (1.x -> 2.x).


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
