---
myst:
  html_meta:
    "description": "Authorize for working in another role. Get environment information."
    "property=og:description": "Authorize for working in another role. Get environment information."
    "property=og:title": "Environment"
    "keywords": "authorization, Plone, API, development"
---

```{eval-rst}
.. currentmodule:: plone.api.env
```
% The Sphinx directive `currentmodule` is used to both run `code-block` examples via [Manuel](https://manuel.readthedocs.io/en/latest/#code-blocks-1) and to avoid duplicating an index entry that is already provided by its counterpart in `docs/api/*.md`.


(chapter-env)=

# Environment

(env-adopt-roles-example)=

## Switch roles inside a block

To temporarily override the list of available roles, use {meth}`api.env.adopt_roles`.
This is especially useful in unit tests.

```python
from plone import api
from AccessControl import Unauthorized

portal = api.portal.get()
with api.env.adopt_roles(['Anonymous']):
    self.assertRaises(
       Unauthorized,
       lambda: portal.restrictedTraverse("manage_propertiesForm")
    )

with api.env.adopt_roles(['Manager', 'Member']):
    portal.restrictedTraverse("manage_propertiesForm")
```

(env-adopt-user-example)=

## Switch user inside a block

To temporarily override the currently active user, use {meth}`api.env.adopt_user`.

```python
from plone import api

portal = api.portal.get()

# Create a new user.
api.user.create(
    username="doc_owner",
    roles=('Member', 'Manager',),
    email="new_owner@example.com",
)

# Become that user and create a document.
with api.env.adopt_user(username="doc_owner"):
    api.content.create(
        container=portal,
        type='Document',
        id='new_owned_doc',
    )

self.assertEqual(
    portal.new_owned_doc.getOwner().getId(),
    "doc_owner",
)
```

(env-debug-mode-example)=

## Debug mode

To know if your Zope instance is running in debug mode, use {meth}`api.env.debug_mode`.

```python
from plone import api

in_debug_mode = api.env.debug_mode()
if in_debug_mode:
    print('Zope is in debug mode')
```

(env-test-mode-example)=

## Test mode

To know if your Plone instance is running in a test runner, use {meth}`api.env.test_mode`.

```python
from plone import api

in_test_mode = api.env.test_mode()
if in_test_mode:
    pass  # do something
```

(env-read-only-mode-example)=

## Read-Only mode

To know if your Zope / Plone instance is running on a read-only ZODB connection use {meth}`api.env.read_only_mode`.

**Use-Case:**
If you run a ZRS or RelStorage cluster with active replication where all replicas are read-only be default.
You could check if your instance is connected to a read only ZODB or a writeable ZODB.
Therefore you could adjust the UI to prevent create, delete or update pages are shown.

```python
from plone import api

is_read_only = api.env.read_only_mode()
if is_read_only:
    pass  # do something
```

(env-plone-version-example)=

## Plone version

To know which version of Plone you are using, use {meth}`api.env.plone_version`.

```python
from plone import api

plone_version = api.env.plone_version()
if plone_version < '4.1':
    pass  # do something
```

(env-zope-version-example)=

## Zope version

To know which version of Zope 2 you are using, use {meth}`api.env.zope_version`.

```python
from plone import api

zope_version = api.env.zope_version()
if zope_version >= '2.13':
    pass  # do something
```

## Further reading

For more information on possible flags and usage options please see the full {ref}`plone-api-env` specification.
