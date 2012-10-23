.. line-block::

    WARNING: If you are reading this on GitHub, DON'T! Read it on ReadTheDocs:
    http://ploneapi.readthedocs.org/en/latest/index.html so you have working
    references and proper formatting.


*******************************
A Plone API
*******************************

.. topic:: Overview

    The :mod:`plone.api` is an elegant and simple API, built for humans wishing
    to develop with Plone.

    It comes with *cookbook*-like documentation with step-by-step instructions
    for doing common development tasks in Plone. Recipes try to assume the user
    does not have extensive knowledge about Plone internals.

The intention of this package is to be transitional. It points out which parts
of Plone are particularly nasty -- we wish they get fixed so we can deprecate
*plone.api* methods that cover them up, but leave the documentation in place.

Some parts of documentation already are this way: they don't use *plone.api*
methods directly, but simply provide guidance on achiving a task using Plone's
internals. Example: usage of the catalog in :ref:`content_find_example`.

The intention is to cover 20% of tasks we do 80% of the time. Keeping everything
in one place helps keep the API introspectable and discoverable, which are
important aspects of being Pythonic.

.. note::

    This package is still in development. It's currently in Beta phase, meaning
    that most stuff should work, but some methods might still change in the
    future, breaking backwards compatibility. Keep that in mind when using it.


Narrative documentation
=======================

.. toctree::
    :maxdepth: 2

    about.rst
    portal.rst
    content.rst
    user.rst
    group.rst


Complete API and advanced usage
===============================

.. toctree::
    :maxdepth: 1

    api/index.rst
    api/portal.rst
    api/content.rst
    api/user.rst
    api/group.rst
    api/exceptions.rst


Contributing
============

.. toctree::
    :maxdepth: 2

    contribute/index.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
