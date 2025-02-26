---
myst:
  html_meta:
    "description": "Inspiration for creating an API. Design decisions for an intuitive usage in common development tasks."
    "property=og:description": "Inspiration for creating an API. Design decisions for an intuitive usage in common development tasks."
    "property=og:title": "About"
    "keywords": "inspiration, design decisions, Plone, development, API"
---

# About

## Inspiration

We want `plone.api` to be developed with [PEP 20](https://peps.python.org/pep-0020/) idioms in mind, in particular:

> Explicit is better than implicit.
>
> Readability counts.
>
> There should be one—and preferably only one—obvious way to do it.
>
> Now is better than never.
>
> If the implementation is hard to explain, it's a bad idea.
>
> If the implementation is easy to explain, it may be a good idea.

All contributions to `plone.api` should keep these rules in mind.

Two libraries are especially inspiring:

[SQLAlchemy](https://www.sqlalchemy.org/)
: Arguably, the reason for SQLAlchemy's success in the developer community lies as much in its feature set as in the fact that its API is very well-designed, is consistent, explicit, and easy to learn.

[Requests](https://requests.readthedocs.io/en/latest/)
: If you look at the documentation for this library, or see [the comparison between the urllib2 way and the requests way](https://gist.github.com/kennethreitz/973705), you can see a parallel for Plone regarding the way we *have been* versus the way we *should be* writing code.
  At the very least, we should have the option of being able to write such clean code.

The API provides grouped functional access to otherwise distributed logic in Plone.
This distribution is a result of two historical factors: reuse of CMF- and Zope-methods, and reasonable but hard to remember splits like `acl_users` and `portal_memberdata`.
Methods defined in `plone.api` implement best-practice access to the original distributed APIs.
These methods also provide clear documentation of how best to access Plone APIs directly.

```{note}
If you doubt those last sentences:
We had five different ways to get the portal root with different edge-cases.
We had three different ways to move an object.
With this in mind, it's obvious that even the simplest Plone tasks can't be documented in a sane way.
```

We do not intend to cover all possible use-cases, only the most common.
We will cover the 20% of possible tasks on which we spend 80% of our time.
If you need to do something that `plone.api` does not support, use the underlying APIs directly.
We try to document sensible use cases even when we don't provide APIs for them, though.

## Design decisions

### Import and usage style

API methods are grouped according to what they affect.
For example:
{ref}`chapter-portal`,
{ref}`chapter-content`,
{ref}`chapter-users`,
{ref}`chapter-groups`,
{ref}`chapter-relation` and
{ref}`chapter-env`.
In general, importing and using an API looks something like this:

% invisible-code-block: python
%
% from plone import api
% api.portal.set_registry_record('plone.use_email_as_login', True)

```python
from plone import api

portal = api.portal.get()
catalog = api.portal.get_tool(name="portal_catalog")
user = api.user.create(email='alice@plone.org')
```

% invisible-code-block: python
%
% self.assertEqual(portal.__class__.__name__, 'PloneSite')
% self.assertEqual(catalog.__class__.__name__, 'CatalogTool')
% self.assertEqual(user.__class__.__name__, 'MemberData')

Always import the top-level package
(`from plone import api`)
and then use the module namespace to access the method you want
(`portal = api.portal.get()`).

All example code should adhere to this style, to encourage one and only one preferred way of consuming API methods.

### Prefer keyword arguments

We prefer using keyword arguments to positional arguments.
Example code in `plone.api` will use this style, and we recommend users follow this convention.
For the curious, here are the reasons why:

1. There will never be any doubt when writing a method whether an argument should be positional or not.
   Decision already made.
2. There will never be any doubt when using the API on which argument comes first, or which ones are named/positional.
   All arguments are named.
3. When using positional arguments, the method signature is dictated by the underlying implementation
   (think required vs. optional arguments).
   Named arguments are always optional in Python.
   Using keywords allows implementation details to change while the signature is preserved.
   In other words, the underlying API code can change substantially but code using it will remain valid.
4. The arguments can all be passed as a dictionary.

```python
# GOOD
from plone import api
alice = api.user.get(username='alice@plone.org')

# BAD
from plone.api import user
alice = user.get('alice@plone.org')
```

## FAQ

### Why aren't we using wrappers?

We could wrap an object (like a user) with an API to make it more usable right now.
That would be an alternative to the convenience methods.

Unfortunately a wrapper is not the same as the object it wraps, and answering the inevitable questions about this difference would be confusing. Moreover, functionality provided by {mod}`zope.interface` such as annotations would need to be proxied.
This would be extremely difficult, if not impossible.

It is also important that developers be able to ensure that their tests continue to work even if wrappers were to be deprecated.
Consider the failure lurking behind test code such as this:

```
if users['bob'].__class__.__name__ == 'WrappedMemberDataObject':
    # do something
```

### Why `delete` instead of `remove`?

- The underlying code uses method names similar to *delete* rather than to *remove*.
- The `CRUD` verb is *delete*, not *remove*.
