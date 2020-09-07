Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

1.10.3 (2020-09-07)
-------------------

Bug fixes:


- Fixed deprecation warning for ``CMFPlone.interfaces.ILanguageSchema``.
  [maurits] (#3130)


1.10.2 (2020-04-20)
-------------------

Bug fixes:


- Minor packaging updates. (#1)


1.10.1 (2020-03-04)
-------------------

Bug fixes:


- Remove deprecation warnings [ale-rt] (#432)
- In tests, use stronger password.
  [maurits] (#436)
- Removed duplicate and failing inline doctest for content.find.
  [maurits] (#437)


1.10.0 (2019-05-01)
-------------------

New features:


- Gracefully handle missing registry records on an interface.
   [gforcada] (#428)


1.9.2 (2019-03-04)
------------------

Bug fixes:


- Fix querying ``object_provides`` for multiple interfaces using 'and'
  operator. [fRiSi] (#426)


1.9.1 (2018-11-20)
------------------

Bug fixes:

- Show only local roles when inherit=False.
  [tschorr]


1.9.0 (2018-09-27)
------------------

New features:

- Python 2/3 support.
  [pbauer]


1.8.5 (2018-09-14)
------------------

Bug fixes:

- Removed allow-hosts from base.cfg, so we can use the new pypi warehouse.
  Refs https://github.com/plone/plone.api/issues/403
  [jaroel]

- fix typos in doc strings
  [tkimnguyen]

- Fix failing AT Collection creation when using api.content.create.
  [gbastien]


1.8.4 (2018-04-24)
------------------

Bug fixes:

- Call ``processForm`` with ``{None: None}`` dict as values.
  This prevents ``processForm`` using ``REQUEST.form`` and overwriting
  values already set by ``invokeFactory``.
  Fixes `issue 99 <https://github.com/plone/plone.api/issues/99>`_.
  [david-batranu]

- Simplification/minor speedup:
  Permissions checks now directly use AccessControl.
  Technical its now exact the same as before.
  Before a tool lookup was needed, calling a utility function, calling AccessControl.
  [jensens]



1.8.3 (2018-02-23)
------------------

Bug fixes:

- Improved code quality according to isort and flake8.  [maurits]

- Fixed regular expression in test for Plone version.  [maurits]


1.8.2 (2018-01-17)
------------------

Bug fixes:

- Fix test in Zope4,
  where ``Products.PlonePAS.tools.memberdata.MemberData`` is an adapter now.
  It can't be proofed to be equal when fetched twice.
  [jensens]

- Change api.group.get_groups to work with CMF master.
  [jaroel]

- Added six to deal with Python 2 / 3 compatibility.
  [rudaporto]

1.8.1 (2017-10-17)
------------------

Bug fixes:

- Don't rename an object when the id already is the target id.
  Fixes `issue 361 <https://github.com/plone/plone.api/issues/361>`_.
  [jaroel]

- Change content.delete to allow both obj=None and objects=[] or objects=None.
  Fixes `issue 383 <https://github.com/plone/plone.api/issues/383>`_.
  [jaroel]

- Let ``zope.i18n`` do the language negotiation for our ``translate`` function.
  Our ``get_current_translation`` does not always give the correct one, especially with combined languages:
  ``nl-be`` (Belgian/Flemish) should fall back to ``nl`` (Dutch).
  The correct negotiated language can also differ per translation domain, which we do not account for.
  ``zope.i18n`` does that better.
  Fixes `issue 379 <https://github.com/plone/plone.api/issues/379>`_.
  [maurits]

- Fix use of Globals.DB which was removed in Zope4 (Fix https://github.com/plone/plone.api/issues/385)
  [pbauer]

1.8 (2017-08-05)
----------------

New features:

- Add method to check if ZODB is in read-only mode.
  [loechel]

- added tox.ini and code convention definitions in setup.py and .editorconfig so that they could be enforced
  [loechel]

Bug fixes:

- Fixes Tests and code convention son this repository.
  [loechel]


1.7 (2017-05-23)
----------------

New features:

- Add disable_roles_acquisition and enable_roles_acquisition to api.content
  [MrTango]

Bug fixes:

- Simplify the ``plone.api.content.delete`` method.
  [thet]

- content.copy with safe_id=False should raise it's own exeception. Fixes #340
  [jaroel]


1.6.1 (2017-03-31)
------------------

Bug fixes:

- Simplify delete and transition functions.
  [adamcheasley]

- Do not reassign dynamic roles as local roles when using user.grant_roles().
  Fixes same issue as #351 for groups.
  [pbauer]

- Include local roles granted from being in a group when using "inherit=False"
  in user.get_roles. Fixes #346
  [pbauer]

- Ignore local roles granted on parents when using "inherit=False" in either
  user.get_roles or group.get_roles. Fixes #354
  [pbauer]

- Fix title wrongly set by ``api.content.create`` when called from GS setup
  handler https://github.com/plone/plone.api/issues/99
  [gotcha, pgrunewald]

1.6 (2017-02-15)
----------------

New features:

- Passing inherit=False to groups.get_roles() will only get local roles for the group.
  [pbauer]

Bug fixes:

- Support user.get_roles for anonymous users. Refs #339
  [jaroel]

- Fix imports from Globals that was removed in Zope4
  [pbauer]

- Fix 'bad' quotes.
  [adamcheasley]

- Typo in the documentation.
  [ale-rt]

- Fix error in tests that try to add built-in roles, which no longer fails
  silently in Zope4.
  [MatthewWilkes]

- Do not reassign global roles as local roles when using group.grant_roles()
  [pbauer]

- reST syntax in documentation, follow style-guide, adjust setup.py
  [svx]

- Do not reassign dynamic roles as local roles when using group.grant_roles().
  [pbauer]

1.5.1 (2016-12-06)
------------------

New:

- `api.portal.get_registry_record` supports an optional `default` parameter
  [ale-rt]

Fixes:

- Fix translation related tests to use the ``plonelocales`` domain instead ``passwordresettool``.
  Products.PasswordResetTool was removed in Plone 5.1.
  [thet]

- Allow plone.api.group.get_groups for Anonymous user. Refs #290
  [jaroel]

- Allow adopting to a Special User. Fixes #320 - checking permissions for Anonymous User.
  [jaroel]

- Fix an AttributeError in `api.user.revoke_roles`
  [ale-rt]

- Remove print statements and use @security decorators to make
  code-analysis happy.
  [ale-rt]

- Typo in the documentation.
  [ale-rt]

- Fix travis and coveralls.
  [gforcada]

- Various wording tweaks
  [tkimnguyen]

- In api.content.move if source **and** target are specified and target is already
  source parent, skip the operation.

- Fix test
  [gforcada]

- Fix PRINTINGMAILHOST_ENABLED evaluation to respect Products.PrintingMailHost
  internal logic
  [ale-rt]

1.5 (2016-02-20)
----------------

New:

- Add `portal.translate`
  [ebrehault]

- Add `portal.get_default_language` and `portal.get_current_language`
  [ebrehault]

Fixes:

- Fix ``test_zope_version`` test to be able to deal with development versions of Zope.
  [thet]

- Remove the Plone APIs conventions. They are moved to
  http://docs.plone.org/develop/styleguide
  and http://docs.plone.org/develop/coredev/docs/git.html
  [thet]

- Cleanup code to match Plone's style guide.
  [gforcada]

- Fix corner case on content.transition code: if a transition only has
  exit transitions and no transition goes back to it ``find_path`` will fail.
  [gforcada]

- Handle automatic transitions on api.content.transition.
  [gforcada]

1.4.11 (2016-01-08)
-------------------

New:

- Allow to set/get registry settings from an interface.
  https://github.com/plone/plone.api/issues/269
  [gforcada]


1.4.10 (2015-11-19)
-------------------

Fixes:

- Rerelease, as 1.4.9 misses the doctests directory.
  [maurits]


1.4.9 (2015-11-19)
------------------

Fixes:

- #283 portal.send_email does not respect transaction aborts
  [jensens]


1.4.8 (2015-10-27)
------------------

New:

- update documentation links, we live in docs.plone.org/develop/plone.api now
  [polyester]

Fixes:

- Fixed Plone 5 version comparison in tests.
  [maurits]


1.4.7 (2015-09-27)
------------------

- Get email_charset value from the configuration registry, falling back
  to portal property if not found.
  [esteele]


1.4.6 (2015-09-14)
------------------

- Fixed `api.content.find` with combination of depth and path.  Path
  is no longer ignored then.
  [maurits]

- Remove unittest2 dependency.
  [gforcada]


1.4.5 (2015-09-09)
------------------

- Fixed long description of package to be valid restructured text,
  displaying nicely on PyPI.
  [maurits]


1.4.4 (2015-09-08)
------------------

- Symlink doctests so that they'll be included in the built egg and don't
  break coredev builds.
  [esteele]


1.4.3 (2015-09-08)
------------------

- Try to get use_email_as_login from registry first.
  [pbauer]


1.4.2 (2015-09-07)
------------------

- Use the version defined in Products.CMFPlone in env.plone_version, just like Plone's control panel.
  Also fixes Jenkins testrunner where we don't have the Plone egg.
  [jaroel]


1.4.1 (2015-09-07)
------------------

- Removed dependency on Products.CMFPlone to avoid circular dependencies. Products.CMFPlone will be there.
  [jaroel]


1.4 (2015-09-04)
----------------

- plone.api.content.delete: add option check_linkintegrity. If True raise
  exception if deleting would result in broken links.
  [pbauer]

- plone.api.content.find: object_provides arguments accepts tuples.
  Fixes #266.
  [ale-rt]

- Fixed plone.api.content.create in Plone 5. Refs 160.
  [jaroel]
- plone.api.content.transition: Now accepts kwargs that can be supplied to the workflow transition.
  [neilferreira]

1.3.3 (2015-07-14)
------------------

- plone.api.content.get_state now allows for an optional default value.
  This is used when no workflow is defined for the object. Refs #246
  [jaroel]

- plone.api.portal.get_registry_record now suggests look-alike records when no records is found. Refs #249.
  [jaroel]

- Fixed tests for Plone 5. Refs #241.
  [jaroel]

- Support Products.PrintingMailHost. Refs #228.
  [jaroel]

- api.plone.org docs point to docs.plone.org/external/plone.api/docs/. Refs #202
  [jaroel]

- plone.api.content.get_view no longer swallows exceptions.
  [jaroel]

- Add plone.api.content.find. Refs #210
  [jaroel]

- Make send_email compatible with Plone >= 5.0b2.
  [pbauer]

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
