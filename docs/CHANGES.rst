Changelog
=========

1.3.3 (unreleased)
------------------

- Use the source's parent as a target when no target is specified.
  [jaroel]

- Make Products.Archetypes dependency optional. Fixes #197
  [jaroel]

- Added local TOCS to main docs pages. Fixes #90.
  [jaroel]

- Allow deleting multiple objects. Fixes #198
  [jaroel]

- Fixed `make docs`.
  [jaroel]

- Support Zope users in user.adopt_user. Fixes #171 and #157.
  [jaroel]

- explicit dependencies in setup.py, explicit zcml loading in tests.
  [jensens]

- import getToolByName from origin location
  [jensens]

- overhaul of documentation: semantic linebreaks, few links fixed, minor
  rewording.
  [jensens]

- fix ``revoke_roles`` method: now if is't called with obj parameter,
  it doesn't set inherited roles locally.
  [cekk]

1.3.2 (2014-11-17)
------------------

- fixes #190 - broken ``MANIFEST.in``.
  [jensens]


1.3.1 (2014-11-17)
------------------

- Resolves issues with ``README.rst`` symlink that prevented 1.3.0 from
  being installed. And please never ever in future use symlinks in eggs, ok?
  [jensens]


1.3.0 (2014-11-17)
------------------

- Fixes #184 NameChooser on rename used the wrong way and fails on
  safe_id=True.
  [benniboy]

- Clarified documentation for content.copy, refs #185.
  [benniboy]

- Fixes if a content is copied in the same folder or in a target folder, where
  same source id exists, the existing source(same folder) or third object
  (same id as source) gets renamed instead of the target.
  [benniboy]

- Use getUserById to find the user when given a User object in adopt_user.
  [tschanzt]

- Made ``api.portal.get_localized_time`` also work with datetime.date.
  [nightmarebadger]

- Raise better/expected errors in ``api.user.grant_roles`` and
  ``api.user.revoke_roles``.
  [adamcheasley]

- Add ``api.user.has_permission`` ref #172.
  [adamcheasley]


1.2.1 (2014-06-24)
------------------

- Resolve issues with CHANGES.rst symlink that prevented 1.2.0 from
  being installed in some circumstances.
  [mattss]


1.2.0 (2014-06-24)
------------------

- Enhance ``api.content.transition`` with the ability to transition from the
  current state to a given state without knowing the transition 'path'
  refs. #162
  [adamcheasley]

- Add ``api.env.plone_version()`` and ``api.env.zope_version()``, refs #126.
  [hvelarde]

- Stop UnicodeDecodeErrors being swallowed in ``api.content.create``.
  [mattss]

- Catch AttributeError in ``api.content.get`` (raised if only part of the
  traversal path exists).
  [mattss]


1.1.0 (2013-10-12)
------------------

- List supported Plone versions in setup.py.
  [zupo]

- Plone 4.0 and 4.1 are now tested under Python 2.6 on CI.
  [hvelarde]

- Use Plone 4.3 on development by default (was 4.2).
  [hvelarde]


1.1.0-rc.1 (2013-10-10)
-----------------------

- Fix README.rst so it renders correctly on PyPI.
  [zupo]

- Use api.plone.org/foo redirects.
  [zupo]

- Add MANIFEST.in file.
  [hvelarde]


1.0.0-rc.3 (2013-10-09)
-----------------------

- Packaging issues.
  [zupo]


1.0.0-rc.2 (2013-10-09)
-----------------------

- Proof-read the docs, improved grammar and wording.
  [cewing]

- Add plone.recipe.codeanalysis to our buildout.
  [flohcim]

- Make all assertRaise() calls use the `with` keyword.
  [winstonf88]

- Amend user.get method to accept a userid parameter, refs #112.
  [cewing, xiru, winstonf88]

  .. note::
    This change fixes a bug in the earlier implementation that could cause
    errors in some situations. This situation will only arise if the userid and
    username for a user are not the same. If membrane is being used for content-
    based user objects, or if email-as-login is enabled *and* a user has changed
    their email address this will be the case. In the previous implementation
    the username parameter was implicitly being treated as userid. The new
    implementation does not do so. If consumer code is relying on this bug and
    passing userid, and if that code uses the username parameter as a keyword
    parameter, then lookup will fail. In all other cases, there should be no
    difference.

- Add api.env.debug_mode() and api.env.test_mode(), refs #125.
  [sdelcourt]

- Move most of text from docs/index.rst to README.rst so its also visible on
  PyPI and GitHub.
  [zupo]

- Deprecate plone.api on ReadTheDocs and redirect to api.plone.org, refs #130.
  [wormj, zupo]

- Add a new `make coverage` command and add support for posting coverage to
  Coveralls.io.
  [zupo]

- Make api.content.create() also print out the underlying error, refs #118.
  [winston88]

- Fix api.content copy/move/rename functions to return the object after they
  change content, refs #115.
  [rodfersou]

- Make Travis IRC notification message to be one-line instead of three-lines.
  [zupo]

- More examples of good and bad code blocks in documentation, more information
  on how to write good docstrings.
  [zupo]

- Prefer single quotes over double quotes in code style.
  [zupo]

- New bootstrap.py to stay in the land of zc.buildout 1.x.
  [zupo]

- Package now includes a copy of the GPLv2 license as stated in the GNU
  General Public License documentation.
  [hvelarde]

- Fixed copying folderish objects.
  [pingviini]

- Fixed moving folderish objects.
  [pingviini]


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
