:orphan:

Changes
=======

1.0.0-rc.1 (2013-01-27)
-----------------------

- Increase test coverage.
  [cillianderoiste, JessN, reinhardt, zupo]

- Implementation of ``api.env.adopt_roles()`` context manager for
  temporarily switching roles inside a block.
  [RichyB]

- Created ``api.env`` module for interacting with global environment.
  [RichyB]

- Decorators for defining constraints on api methods. Depend on `decorator`
  package.
  [JessN]

- Resolved #61: Improve api.portal.get().
  [cillianderoiste]

- Use plone.api methods in plone.api codebase.
  [zupo]

- Switch to `flake8` instead of `pep8`+`pyflakes`.
  [zupo]

- Get the portal path with absolute_url_path.
  [cillianderoiste]

- Travis build speed-ups.
  [zupo]

- Support for Python 2.6.
  [RichyB, zupo]

- Support for Plone 4.0.
  [adamcheasley]

- Support for Plone 4.3.
  [cillianderoiste, zupo]

- Spelling fixes.
  [adamtheturtle]

- Make get_view and get_tool tests not have hardcoded list of *all* expected
  values.
  [RichyB, cillianderoiste]

- Code Style Guide.
  [iElectric, cillianderoiste, marciomazza, RichyB, thet, zupo]

- Depend on ``manuel`` in setup.py.
  [zupo]

- Documentation how to get/set member properties.
  [zupo]

- Improvements to ``get_registry_record``.
  [zupo]


0.1b1 (2012-10-23)
------------------

- Contributors guide and style guide.
  [zupo]

- Enforce PEP257 for docstrings.
  [zupo]

- Fix ``get_navigation_root()`` to return object instead of path.
  [pbauer]

- Implementation of ``get_permissions()``, ``get_roles()``,
  ``grant_roles()`` and ``revoke roles()`` for users and groups.
  [rudaporto, xiru]

- Implementation of ``get_registry_record`` and ``set_registry_record``.
  [pbauer]

- Use `Makefile` to build the project, run tests, generate documentation, etc.
  [witsch]

- Moving all ReadTheDocs dependencies into ``rtd_requirements.txt``.
  [zupo]


0.1a2 (2012-09-03)
------------------

- Updated release, adding new features, test coverage, cleanup & refactor.
  [hvelarde, avelino, ericof, jpgimenez, xiru, macagua, zupo]


0.1a1 (2012-07-13)
------------------

- Initial release.
  [davisagli, fulv, iElectric, jcerjak, jonstahl, kcleong, mauritsvanrees,
  wamdam, witsch, zupo]


