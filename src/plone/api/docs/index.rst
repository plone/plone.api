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
