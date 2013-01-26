:orphan:

Changes
=======

0.1b2 (Unreleased)
------------------

- Improvements to ``get_registry_record``.
  [zupo]

- Created ``api.env`` module for interacting with global environment.

- Implementation of ``api.env.adopt_roles()`` context manager for
  temporarily switching roles inside a block.

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


