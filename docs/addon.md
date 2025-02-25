---
myst:
  html_meta:
    "description": "Get and manage addons"
    "property=og:description": "Get, modify and manage addons"
    "property=og:title": "Addons"
    "keywords": "Plone, API, development"
---

```{eval-rst}
.. module:: plone.api.addon
```

(chapter-addons)=

# Addon

(addons-get-addons)=

## Get addons

To get all the addons present in the current Plone site, use the {func}`api.addon.get_addons` function.
The function accepts an optional `limit` parameter to filter the returned addons.

```python
from plone import api

# Get all addons
addons = api.addon.get_addons()

# Get only installed addons
installed = api.addon.get_addons(limit='installed')

# Get only upgradable addons
upgradable = api.addon.get_addons(limit='upgradable')

# Get only broken addons
broken = api.addon.get_addons(limit='broken')

# Get IDs of installed addons
addon_ids = api.addon.get_addon_ids(limit='installed')
```

The `limit` parameter accepts these values:
- `installed`: Return only installed addons.
- `upgradable`: Return only addons that can be upgraded.
- `broken`: Return broken addons.
- `non_installable`: Return non-installable addons.

## Get addon information

To get information about a specific addon.

```python
from plone import api

addon = api.addon.get('plone.app.multilingual')
print(addon.id)           # ID of the addon
print(addon.version)      # Version string
print(addon.title)        # Display title
print(addon.description)  # Description
print(addon.flags)        # List of flags like ['installed', 'upgradable']
```

## Install and uninstall addons

To install an addon:

```python
from plone import api

success = api.addon.install('plone.app.multilingual')
```

To uninstall an addon:

```python
from plone import api

success = api.addon.uninstall('plone.app.multilingual')
```

## Get addon version

To get the version of an addon.

```python
from plone import api

version = api.addon.get_version('plone.app.multilingual')
```

(addons-exceptions)=

## Exceptions

The following exceptions may be raised.

- {exc}`~plone.api.exc.InvalidParameterError` exception is raised in the following cases:
  - Trying to get information about a non-existent addon
  - Using an invalid limit parameter value

## Further reading

For more information on possible flags and usage options please see the full {ref}`plone-api-addon` specification.
