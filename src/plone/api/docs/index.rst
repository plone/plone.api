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

Ideally we want the API to behave like a dict. In this way you don't
have to remember method names that do CRUD. You just use the API like
you'd use any dict.

However the underlying APIs that plone.api is using (like portal_memberdata, ...)
are not perfect. For tasks where we cannot yet support dict-like API, we
add convenience methods. When the underlying APIs get fixed, we will change
the documentation to point to using the dict-like access and we'll deprecate
the convenience methods.

For example, changing a password. Ideally we want the code to look like this:

  from plone import api
  api.users['bob'].password = "secret"

But currently we must use this:

  from plone import api
  api.set_password('bob', 'secret')


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
