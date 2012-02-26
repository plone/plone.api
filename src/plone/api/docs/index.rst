*******************************
:mod:`plone.api` -- A Plone API
*******************************

:Author: Plone Foundation
:Version: |version|

.. module:: plone.api

.. topic:: Overview

   The :mod:`plone.api` is an elegant and simple API, built for humans wishing
   to develop with Plone.


When documenting plone, an easy and understandable set of basic
functions helps to keep the documentation focused on the current task
and to keep it simple and small.

Instead of documenting the ZCA over and over again, we want to
describe how to work with plone.

In addition we want a simple entry point for the most important tools
that are needed on nearly every project. We will also add helper
methods for things that the tools should already do themselves in an
easy way, but currently don't. Keeping everything in one place helps
keep the API introspectable and discoverable, which are important
aspects of being Pythonic.

Such methods may be deprecated if the underlying tools implement an acceptable
API.

Inspiration
===========
We want `plone.api` to be developed with `PEP 20 <http://www.python.org/dev/peps/pep-0020/>`_ idioms in mind, in particular:

  |   Explicit is better than implicit.
  |   Readability counts.
  |   There should be one-- and preferably only one --obvious way to do it.
  |   Now is better than never.
  |   If the implementation is hard to explain, it's a bad idea.
  |   If the implementation is easy to explain, it may be a good idea.

All contributions to `plone.api` should keep these important rules in mind.

Two libraries are especially inspiring:

`SQLAlchemy <http://www.sqlalchemy.org/>`_
  Arguably, the reason for SQLAlchemy's success in the developer community
  lies as much in its feature set as in the fact that its API is very well 
  designed, is consistent, 
  explicit, and easy to learn.

`Requests <http://docs.python-requests.org>`_
  As of this writing, this is still a very new library, but just looking at 
  `a comparison between the urllib2 way and the requests way <https://gist.github.com/973705>`_,
  as well as the rest of its documentation, one cannot but see a parallel
  between the way we *have been* and the way we *should be* writing code for
  Plone (or at least have that option).


Design decisions
================
No positional arguments.  All named arguments.

Ideally we want the API to behave 'pythonic', i.e. like a dict or set where
appropriate. This way developers don't have to remember method names that
support CRUD of things like users, groups, resources and content.

However, Plone's underlying APIs (like `portal_memberdata` etc) are mostly not
following the same approach. For tasks where no 'pythonic' API exists (yet)
convenience methods are provided. These should be considered to be temporary
or rather transitional, i.e. when the underlying APIs get "fixed", the
practices recommended by i:mode:`plone.api` will be adjusted accordingly and
the convenience methods will be deprecated.

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
