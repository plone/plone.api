=========
Rationale
=========

Inspiration
===========

We want `plone.api` to be developed with `PEP 20
<http://www.python.org/dev/peps/pep-0020/>`_ idioms in mind, in particular:

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
  designed, is consistent, explicit, and easy to learn.

`Requests <http://docs.python-requests.org>`_
  As of this writing, this is still a very new library, but just looking at
  `a comparison between the urllib2 way and the requests way
  <https://gist.github.com/973705>`_, as well as the rest of its documentation,
  one cannot but see a parallel between the way we *have been* and the way we
  *should be* writing code for Plone (or at least have that option).


Design decisions
================

Import and usage style
----------------------

API methods are grouped by their field of usage: portal, view, content, users,
etc. Hence the importing and usage of API methods look like this:

.. code-block:: python

    from plone import api

    portal = api.portal.get()
    url = api.portal.url()
    user = api.user.create('alice@plone.org')

.. invisible-code-block:: python

    self.assertEqual(portal, 'TODO')
    self.assertEqual(url, 'TODO')
    self.assertEqual(user, 'TODO')

In other words, always import the top-level package (``from plone import api``)
and then use the group namespace to access the method you want
(``url = api.portal.url()``).

All example code should adhere to this style, so we encourage one and only
one prefered way of consuming API methods.


Prefer keyword arguments
------------------------

For the following reasons the example code in the API (and hence the
recommendation to people on how to use it) shall always prefer using keyword
instead of positional arguments:

#. There will never be a doubt when writing a method on whether an argument
   should be positional or not.  Decision already made.
#. There will never be a doubt when using the API on which argument comes
   first, or which ones are named/positional.  All arguments are named.
#. When using positional arguments, the method signature is dictated by the
   underlying implementation.  Think required vs. optional arguments.  Named
   arguments are always optional in Python.  This allows us to change
   implementation details and leave the signature unchanged. In other words,
   the underlying API code can change substantially and the code using it will
   remain valid.
#. The arguments can all be passed as a dictionary.

The API provides grouped functional access to otherwise distributed logic
in Plone. Plone's original distribution of logic is a result of two things:
The historic re-use of CMF- and Zope-methods and reasonable, but
at first hard to understand splits like acl_users.* and portal_memberdata.

So we created some modules with a bunch of useful methods that implement
best-practice access to the original distributed APIs. In this way we also
document in code how to use Plone directly.

.. note ::
   If you doubt those last sentences: We had five different ways to get the
   site root with different edge-cases. We had three different ways to move
   an object. With this in mind, it's obvious that even the most simple
   tasks can't be documented in Plone in a sane way.

Also, we don't intend to cover all possible use-cases. Only the absolutely
most common ones. If you need to do something that `plone.api` does not support,
just use the underlaying APIs directly. We will cover 20% of tasks that are
being done 80% of the time, and not one more.


FAQ
===

Why aren't we using wrappers?
-----------------------------

We could wrap an object (like a user) with an API to make it more usable
right now. That would be an alternative to the convenience methods.

But telling developers that they will get yet another object from the API which
isn't the requested object, but a API-wrapped one instead, would be very hard.
Also, making this wrap transparent, in order to make the returned object
directly usable, would be nearly impossible, because we'd have to proxy all the
:mod:`zope.interface` stuff, annotations and more.

Furthermore, we want to avoid people writing code like this in tests or their
internal utility code and failing miserably in the future if wrappers would
no longer be needed and would therefore be removed::

    if users['bob'].__class__.__name__ == 'WrappedMemberDataObject':
        # do something


Why ``delete`` instead of ``remove``?
-------------------------------------

* The underlying code uses methods that are named more similarly to *delete*
  rather than to *remove*
* ``CRUD`` has *delete*, not *remove*.
