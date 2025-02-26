---
myst:
  html_meta:
    "description": "Get, modify, and manage Plone add-ons"
    "property=og:description": "Get, modify, and manage Plone add-ons"
    "property=og:title": "Get, modify, and manage Plone add-ons"
    "keywords": "Plone, API, development, add-on, manage"
---

```{eval-rst}
.. module:: plone.api.addon
```

(chapter-addons)=

# Add-ons

This chapter describes how to get, update, install, uninstall, and manage Plone add-ons.


(addons-get-addons)=

## Get add-ons

To get all the add-ons present in the current Plone site, use the {func}`api.addon.get_addons` function.
The function accepts an optional `limit` parameter to filter the returned add-ons.
`limit` may be one of the following strings.

`available`
:   Products that are not installed, but could be.

`broken`
:   Uninstallable products with broken dependencies.

`installed`
:   Only products that are installed and not hidden.

`non_installable`
:   Non-installable products.

`upgradable`
:   Only products with upgrades.

The following examples demonstrate usage of the {func}`api.addon.get_addons` function.

```python
from plone import api

# Get all add-ons
addons = api.addon.get_addons()

# Get only installed add-ons
installed = api.addon.get_addons(limit="installed")

# Get only upgradable add-ons
upgradable = api.addon.get_addons(limit="upgradable")

# Get only broken add-ons
broken = api.addon.get_addons(limit="broken")
```

(addons-get-addon-ids)=

## Get add-on IDs

To get all the add-ons' IDs present in the current Plone site, use the {func}`api.addon.get_addon_ids` function.
The function accepts an optional `limit` parameter to filter the returned add-ons, exactly the same as the {func}`api.addon.get_addons` function.
`limit` may be one of the following strings.

`available`
:   Products that are not installed, but could be.

`broken`
:   Uninstallable products with broken dependencies.

`installed`
:   Only products that are installed and not hidden.

`non_installable`
:   Non-installable products.

`upgradable`
:   Only products with upgrades.

The following examples demonstrates usage of the {func}`api.addon.get_addon_ids` function.

```python
# Get IDs of installed add-ons
addon_ids = api.addon.get_addon_ids(limit="installed")
```
## Get add-on information

To get information about a specific add-on, use the {func}`api.addon.get` function, passing in the name of the add-on as a string.

```python
from plone import api

addon = api.addon.get("plone.session")
print(addon.id)           # ID of the add-on
print(addon.version)      # Version string
print(addon.title)        # Display title
print(addon.description)  # Description
print(addon.flags)        # List of flags like ["installed", "upgradable"]
```

## Install and uninstall add-ons

To install an add-on, use the {func}`api.addon.install` function, passing in the name of the add-on as a string, as shown in the following example.

```python
from plone import api

success = api.addon.install("plone.session")
```

To uninstall an add-on, use the {func}`api.addon.uninstall` function, passing in the name of the add-on as a string, as shown in the following example.


```python
from plone import api

success = api.addon.uninstall("plone.session")
```

## Get add-on version

To get the version of an add-on, use the {func}`api.addon.get_version` function, passing in the name of the add-on as a string, as shown in the following example.

```python
from plone import api

version = api.addon.get_version("plone.session")
```

(addons-exceptions)=

## Exceptions


The {exc}`~plone.api.exc.InvalidParameterError` exception may be raised in the following cases.

- When using the {func}`api.addon.get` function, trying to get information about a non-existent add-on.
- When using either function {func}`api.addon.get_addons` or {func}`api.addon.get_addon_ids`, using an invalid `limit` parameter value.

