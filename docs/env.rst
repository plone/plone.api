.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T!
    Read the documentation at `docs.plone.org <http://docs.plone.org/develop/plone.api/docs/env.html>`_
    so you have working references and proper formatting.


.. module:: plone

.. _chapter_env:

===========
Environment
===========

.. _env_adopt_roles_example:

Switch roles inside a block
===========================

To temporarily override the list of available roles, use :meth:`api.env.adopt_roles`.
This is especially useful in unit tests.

.. code-block:: python

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


.. _env_adopt_user_example:

Switch user inside a block
==========================

To temporarily override the currently active user, use :meth:`api.env.adopt_user`.

.. code-block:: python

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

.. _env_debug_mode_example:

Debug mode
==========

To know if your Zope instance is running in debug mode, use :meth:`api.env.debug_mode`.

.. code-block:: python

    from plone import api

    in_debug_mode = api.env.debug_mode()
    if in_debug_mode:
        print('Zope is in debug mode')


.. _env_test_mode_example:

Test mode
=========

To know if your Plone instance is running in a test runner, use :meth:`api.env.test_mode`.

.. code-block:: python

    from plone import api

    in_test_mode = api.env.test_mode()
    if in_test_mode:
        pass  # do something


.. _env_read_only_mode_example:

Read-Only mode
==============

To know if your Zope / Plone instance is running on a read-only ZODB connection use :meth:`api.env.read_only_mode`.

**Use-Case:**
If you run a ZRS or RelStorage cluster with active replication where all replicas are read-only be default.
You could check if your instance is connected to a read only ZODB or a writeable ZODB.
Therefore you could adjust the UI to prevent create, delete or update pages are shown.

.. code-block:: python

    from plone import api

    is_read_only = api.env.read_only_mode()
    if is_read_only:
        pass  # do something


.. _env_plone_version_example:

Plone version
=============

To know which version of Plone you are using, use :meth:`api.env.plone_version`.

.. code-block:: python

    from plone import api

    plone_version = api.env.plone_version()
    if plone_version < '4.1':
        pass  # do something


.. _env_zope_version_example:

Zope version
============

To know which version of Zope 2 you are using, use :meth:`api.env.zope_version`.

.. code-block:: python

    from plone import api

    zope_version = api.env.zope_version()
    if zope_version >= '2.13':
        pass  # do something


Further reading
===============

For more information on possible flags and usage options please see the full :ref:`plone-api-env` specification.
