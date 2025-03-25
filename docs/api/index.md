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

addon
content
env
exceptions
group
portal
relation
user
```


## `api.addon`

```{eval-rst}
.. autosummary::

    api.addon.AddonInformation
    api.addon.NonInstallableAddons
    api.addon.get
    api.addon.get_addon_ids
    api.addon.get_addons
    api.addon.get_version
    api.addon.install
    api.addon.uninstall
```


## `api.content`

```{eval-rst}
.. autosummary::

    api.content.copy
    api.content.create
    api.content.delete
    api.content.disable_roles_acquisition
    api.content.enable_roles_acquisition
    api.content.find
    api.content.get
    api.content.get_closest_ancestor
    api.content.get_state
    api.content.get_uuid
    api.content.get_view
    api.content.get_path
    api.content.get_state
    api.content.get_uuid
    api.content.get_view
    api.content.iter_ancestors
    api.content.move
    api.content.rename
    api.content.transition
```


## `api.env`

```{eval-rst}
.. autosummary::

    api.env.adopt_roles
    api.env.adopt_user
    api.env.debug_mode
    api.env.plone_version
    api.env.read_only_mode
    api.env.test_mode
    api.env.zope_version
```


## `api.exc`

```{eval-rst}
.. autosummary::

    api.exc.CannotGetPortalError
    api.exc.GroupNotFoundError
    api.exc.InvalidParameterError
    api.exc.MissingParameterError
    api.exc.PloneApiError
    api.exc.UserNotFoundError
```


## `api.group`

```{eval-rst}
.. autosummary::

    api.group.add_user
    api.group.create
    api.group.delete
    api.group.get
    api.group.get_groups
    api.group.get_roles
    api.group.grant_roles
    api.group.remove_user
    api.group.revoke_roles
```


## `api.portal`

```{eval-rst}
.. autosummary::

    api.portal.get
    api.portal.get_current_language
    api.portal.get_default_language
    api.portal.get_localized_time
    api.portal.get_navigation_root
    api.portal.get_registry_record
    api.portal.get_tool
    api.portal.get_vocabulary
    api.portal.get_vocabulary_names
    api.portal.send_email
    api.portal.set_registry_record
    api.portal.show_message
    api.portal.translate
```


## `api.relation`

```{eval-rst}
.. autosummary::

    api.relation.create
    api.relation.delete
    api.relation.get
```


## `api.user`

```{eval-rst}
.. autosummary::

    api.user.create
    api.user.delete
    api.user.get
    api.user.get_current
    api.user.get_permissions
    api.user.get_roles
    api.user.get_users
    api.user.grant_roles
    api.user.has_permission
    api.user.is_anonymous
    api.user.revoke_roles
```
