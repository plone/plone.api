.. line-block::

    WARNING: If you are reading this on GitHub, DON'T! Read it on ReadTheDocs:
    http://ploneapi.readthedocs.org/en/latest/about.html so you have working
    references and proper formatting.


=====
About
=====

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

The API provides grouped functional access to otherwise distributed logic
in Plone. Plone's original distribution of logic is a result of two things:
The historic re-use of CMF- and Zope-methods and reasonable, but
at first hard to understand splits like acl_users.* and portal_memberdata.

That's why we've created a set of useful methods that implement best-practice
access to the original distributed APIs. In this way we also document in code
how to use Plone directly.

.. note ::
   If you doubt those last sentences: We had five different ways to get the
   portal root with different edge-cases. We had three different ways to move
   an object. With this in mind, it's obvious that even the most simple
   tasks can't be documented in Plone in a sane way.

Also, we don't intend to cover all possible use-cases. Only the most common
ones. If you need to do something that `plone.api` does not support,
just use the underlying APIs directly. We will cover 20% of tasks that are
being done 80% of the time, and not one more. We try to document sensible use
cases even when we don't provide them, though.


Design decisions
================

Import and usage style
----------------------

API methods are grouped by their field of usage. For example:
:ref:`chapter_portal`, :ref:`chapter_content`, :ref:`chapter_users`
and :ref:`chapter_groups`.  Hence the importing and usage of API
methods look like this:

.. invisible-code-block: python

    from plone import api
    portal = api.portal.get()
    portal.portal_properties.site_properties.use_email_as_login = True

.. code-block:: python

    from plone import api

    portal = api.portal.get()
    catalog = api.portal.get_tool(name="portal_catalog")
    user = api.user.create(email='alice@plone.org')

.. invisible-code-block: python

    self.assertEqual(portal.__class__.__name__, 'PloneSite')
    self.assertEqual(catalog.__class__.__name__, 'CatalogTool')
    self.assertEqual(user.__class__.__name__, 'MemberData')

In other words, always import the top-level package (``from plone import api``)
and then use the group namespace to access the method you want
(``portal = api.portal.get()``).

All example code should adhere to this style, so we encourage one and only
one preferred way of consuming API methods.


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


.. code-block:: python

    # GOOD
    from plone import api
    portal = api.portal.get()
    alice = api.user.get(username='alice@plone.org')

    # BAD
    from plone.api import portal, user
    portal = portal.get()
    alie = user.get('alice@plone.org')


FAQ
===

Why aren't we using wrappers?
-----------------------------

We could wrap an object (like a user) with an API to make it more usable
right now. That would be an alternative to the convenience methods.

But telling developers that they will get yet another object from the API which
isn't the requested object, but an API-wrapped one instead, would be very hard.
Also, making this wrap transparent in order to make the returned object
directly usable would be nearly impossible, because we'd have to proxy all the
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


Roadmap
=======

Medium- to long-term:
---------------------

Below is a collection of ideas we have for the long run, in no particular order:

- api.env.adopt_user (to use with ``with``, especially in tests):

  .. code-block:: python

      with api.env.adopt_user('admin'):
          api.context.create(
              type='Document',
              title='Exhaustive list of kittens',
              container=portal
          )
          # Should leave behind a Document object owned by the user 'admin'.

- api.env TEST_MODE and DEBUG_MODE

  .. code-block:: python

      if api.env.TEST_MODE:
          # you are now in test environment

      if api.env.DEBUG_MODE:
          # you are now in development environment

- api.env.versions: don't do a wrapper, just explain how to use pkg_resources
  to query for installed versions

- unify permissions

  - have all different types of permission in one place and one way to use them

- rewrite sub-optimal underlying APIs and deprecate plone.api methods, but leave
  the (updated) documentation:

  - getting/setting member properties
  - tools:

    - portal_groupdata, portal_groups, portal_memberdata, portal_membership
    - portal_quickinstaller, portal_undo

- JSON webservices

  - probably in a separate package plone.jsonapi
  - one view (@@jsonapi for example) that you can call in your JS and be sure it
    won't change
  - easier to AJAXify stuff

- Flask-type url_for_view() and view_for_url()
