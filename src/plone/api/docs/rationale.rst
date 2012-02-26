=========
Rationale
=========

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
No positional arguments.  Only named (keyword) arguments.
  #. There will never be a doubt when writing a method on whether an argument should be positional or not.  Decision already made.
  #. There will never be a doubt when using the API on which argument comes first, and which ones are named.  All arguments are named.
  #. When using positional arguments, the method signature is dictated by the underlying implementation.  Think required vs. optional arguments.  Named arguments are always optional in Python.  This allows us to change implementation details and leave the signature unchanged.
  #. The arguments can all be passed as a dictionary.

Ideally we want the API to behave 'pythonically', i.e. like a dict or set
where appropriate. This way developers need to remember less method names
and just use the API as a dict/set.

However, Plone's underlying APIs (like `portal_memberdata` etc) are suboptimal
in this regard. For tasks where no 'pythonic' API exists (yet), we provide
convenience methods. These should be considered as temporary or rather
transitional solution. I.e. when the underlying APIs get "fixed", the
practices recommended by :mod:`plone.api` will be adjusted accordingly and
the convenience methods will be deprecated.

For example, modifying user's `fullname` property. Ideally we want the code to
look like this:

.. code-block:: python

    from plone import api
    bob = api.users.get(username='bob')
    bob.fullname = 'Bob Smith'

But currently we must use this:

.. code-block:: python

    from plone import api
    bob = api.users.get(username='bob')
    api.users.set_property(user=bob, name='fullname', value='Bob Smith')

.. invisible-code-block:: python

   self.assertEquals(bob.getProperty('fullname'), 'Bob Smith')


In any case: The API will persist even when the convenience methods will be
deprecated.

Also, we don't intend to cover all possible use-cases. Only the absolutely
most common ones. If you need to do something funky, just use the
underlaying APIs directly. We will cover 20% of tasks that are done 80% of
the time, and not one more.


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

Furthermore, we want to avoid people writing code like this in tests of their
internal utility code::

    if users['bob'].__class__.__name__ == 'WrappedMemberDataObject':
        # do something


**Won't dict-access for users encourage developers to mis-use MemberData objects?**

This is a risk, yes. For now, we will make it clear in the documentation of
:mod:`plone.api` what the limitations of users dict are and how to use it
propertly. Big red honking banners should give warning what not to do.

With this we can focus on fixing `portal_memberdata` to not allow developers to
shoot themselves in the knee but rather expose a sane API.
