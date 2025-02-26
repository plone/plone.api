---
myst:
  html_meta:
    "description": "Get and manage add-ons"
    "property=og:description": "Get, modify and manage add-ons"
    "property=og:title": "add-ons"
    "keywords": "Plone, API, development"
---

```{eval-rst}
.. module:: plone.api.addon
```

(chapter-addons)=

# Add-on

(addons-get-addons)=

## Get add-ons

To get all the add-ons present in the current Plone site, use the {func}`api.addon.get_addons` function.
The function accepts an optional `limit` parameter to filter the returned add-ons.

```python
from plone import api

# Get all add-ons
addons = api.addon.get_addons()

# Get only installed add-ons
installed = api.addon.get_addons(limit='installed')

# Get only upgradable add-ons
upgradable = api.addon.get_addons(limit='upgradable')

# Get only broken add-ons
broken = api.addon.get_addons(limit='broken')

# Get IDs of installed add-ons
addon_ids = api.addon.get_addon_ids(limit='installed')
```

The `limit` parameter accepts these values:
- `installed`: Return only installed add-ons.
- `upgradable`: Return only add-ons that can be upgraded.
- `broken`: Return broken add-ons.
- `non_installable`: Return non-installable add-ons.

## Get add-on information

To get information about a specific add-on.

```python
from plone import api

addon = api.addon.get('plone.session')
print(addon.id)           # ID of the add-on
print(addon.version)      # Version string
print(addon.title)        # Display title
print(addon.description)  # Description
print(addon.flags)        # List of flags like ['installed', 'upgradable']
```

## Install and uninstall add-ons

To install an add-on:

```python
from plone import api

success = api.addon.install('plone.session')
```

To uninstall an add-on:

```python
from plone import api

success = api.addon.uninstall('plone.session')
```

## Get add-on version

To get the version of an add-on.

```python
from plone import api

version = api.addon.get_version('plone.session')
```

(addons-exceptions)=

## Exceptions

The following exceptions may be raised.

- {exc}`~plone.api.exc.InvalidParameterError` exception is raised in the following cases:
  - Trying to get information about a non-existent add-on
  - Using an invalid limit parameter value

## Further reading

For more information on possible flags and usage options please see the full {ref}`plone-api-addon` specification.
