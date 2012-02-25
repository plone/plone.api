*******************************
:mod:`plone.api` -- A Plone API
*******************************

:Author: Plone Foundation
:Version: |version|

.. module:: plone.api

.. topic:: Overview

   The :mod:`plone.api` is an attempt to provide an easy to use API
   for developing with Plone.


When documenting plone, an easy and understandable set of basic
functions helps to keep the documentation focused on the current task
and to keep it simple and small.

Instead of documenting the ZCA over and over again, we want to
describe how to work with plone.

In addition we want a simple entry point for the most important tools
that are needed on nearly every project. We will also add helper
methods for things that the tools should already do themselves in an
easy way, but currently don't.

We plan to deprecate such methods as soon as the tools implement an
acceptable API.


Design decisions
================

Ideally we want the API to behave 'pythonic', i.e. like a dict or set where
appropriate. This way developers don't have to remember method names that
support CRUD of things like users, groups, resources and content.

However, Plone's underlying APIs (like `portal_memberdata` etc) are mostly not
following the same approach. For tasks where no 'pythonic' API exists (yet)
convenience methods are provided. These should be considered to be temporary or
rather transitional, i.e. when the underlying APIs get "fixed", the practices
recommended by i:mode:`plone.api` will be adjusted accordingly and the
convenience methods will be deprecated.

For example, changing a password. Ideally we want the code to look like this:

.. code-block:: python

    from plone import api
    api.users['bob'].password = "secret"

But currently we must use this:

.. code-block:: python

    from plone import api
    api.set_password('bob', 'secret')


To be clear: The API will persist even when the convenience methods will be
deprecated.

Also, we don't intend to cover all possible use-cases. Only the absolutely
most common ones. If you need to do something funky, just use the
underlaying APIs directly.


FAQ
===

**Why we don't want to use wrappers**

We could also wrap a object (like a user) with a API to make it more usable
right now. That would be an alternative to the convenience methods.

But telling developers that they will get yet another object from the API which
isn't the requested object, but a API-wrapped one instead, would be very hard.
Also, making this wrap transparent, in order to make the returned object
directly usable, would be nearly impossible, because we'd have to proxy all the
:mod:`zope.interface` stuff, annotations and more.


**Won't dict-access for users encourage developers to mis-use MemberData objects?**

This is a risk, yes. For now, we will make it clear in the documentation of
:mod:`plone.api` what the limitations of users dict are and how to use it
propertly. Big red honking banners should give warning what not to do.

With this we can focus on fixing `portal_memberdata` to not allow developers to
shoot themselves in the knee but rather expose a sane API.


Table of Contents
=================

.. toctree::
   :maxdepth: 2

   content.rst
   users.rst
   utilities.rst
   inittools.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
