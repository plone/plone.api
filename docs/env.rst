.. line-block::

    WARNING: If you are reading this on GitHub, DON'T! Read it on ReadTheDocs:
    http://ploneapi.readthedocs.org/en/latest/env.html so you have working
    references and proper formatting.


.. module:: plone

.. _chapter_env:

Environment
===========

.. _env_adopt_roles_example:

Switch roles inside a block
---------------------------

To temporarily override the list of roles that are available, use
:meth:`api.env.adopt_roles`. This is especially useful in unit tests.

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
--------------------------

To temporarily override the user which is currently active, use
:meth:`api.env.adopt_user`.

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

Further reading
---------------

For more information on possible flags and usage options please see the full
:ref:`plone-api-env` specification.

