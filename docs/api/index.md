---
myst:
  html_meta:
    "description": "Overview of the API methods"
    "property=og:description": "Overview of the API methods"
    "property=og:title": "API methods and descriptions"
    "keywords": "Plone, API, methods, development"
---

```{eval-rst}
.. currentmodule:: plone
```

# API methods and descriptions

```{toctree}
:maxdepth: 1
:hidden: true

portal
content
user
group
env
relation
addon
exceptions
```


## `api.portal`

```{eval-rst}
.. autosummary::

    api.portal.get
    api.portal.get_navigation_root
    api.portal.get_tool
    api.portal.get_localized_time
    api.portal.send_email
    api.portal.show_message
    api.portal.get_registry_record

```

## `api.content`

```{eval-rst}
.. autosummary::

    api.content.get
    api.content.create
    api.content.delete
    api.content.copy
    api.content.move
    api.content.rename
    api.content.get_uuid
    api.content.get_state
    api.content.transition
    api.content.get_view

```

## `api.user`

```{eval-rst}
.. autosummary::

    api.user.get
    api.user.create
    api.user.delete
    api.user.get_current
    api.user.is_anonymous
    api.user.get_users
    api.user.get_roles
    api.user.get_permissions
    api.user.grant_roles
    api.user.revoke_roles

```

## `api.group`

```{eval-rst}
.. autosummary::

    api.group.get
    api.group.create
    api.group.delete
    api.group.add_user
    api.group.remove_user
    api.group.get_groups
    api.group.get_roles
    api.group.grant_roles
    api.group.revoke_roles

```

## `api.env`

```{eval-rst}
.. autosummary::

    api.env.adopt_roles
    api.env.adopt_user
    api.env.debug_mode
    api.env.test_mode

```

## `api.relation`

```{eval-rst}
.. autosummary::

    api.relation.get
    api.relation.create
    api.relation.delete

```

## Exceptions and errors

```{eval-rst}
.. autosummary::

    api.exc.PloneApiError
    api.exc.MissingParameterError
    api.exc.InvalidParameterError
    api.exc.CannotGetPortalError
```
