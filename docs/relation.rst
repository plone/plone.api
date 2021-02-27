.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T!
    Read the documentation at `docs.plone.org <http://docs.plone.org/develop/plone.api/docs/env.html>`_
    so you have working references and proper formatting.


.. module:: plone

.. _chapter_relation:

=========
Relations
=========

Note: the relations code only works for Dexterity content, not for Archetypes.

.. _relation_create_example:

Create relation
===============

To create a relation between source object and target object, use :meth:`api.relation.create`.

.. code-block:: python

    from plone import api

    portal = api.portal.get()
    source = portal.bob
    target = portal.bobby
    api.relation.create(source=source, target=target, relationship="friend")

Delete relation
===============

.. code-block:: python

    api.relation.delete(source=source, target=target, relationship="friend")

In order to delete relation(s), you must provide either the ``source``, ``target`` or ``relationship``.

Get relations
=============

.. code-block:: python

    api.relation.get(source=source, target=target, relationship="friend", unrestricted=False, as_dict=False)

You must provide either source, target or relationship, or a combination of those.
``unrestricted`` and ``as_dict`` are optional.

By default the result is a list of objects.
If you set ``as_dict=True`` it will return a dictionary with the names of the relations as keys and lists of objects as values.

By default the View permission is checked on the relation objects.
You only get objects that you are allowed to see.
Use the ``unrestricted`` parameter if you want to bypass this check.

To get back relations, so relations pointing to an item, use:

.. code-block:: python

    api.relation.get(target=target)


Further reading
===============

For more information on possible flags and usage options please see the full :ref:`plone-api-relation` specification.
