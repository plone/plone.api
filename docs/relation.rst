.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T!
    Read the documentation at `docs.plone.org <http://docs.plone.org/develop/plone.api/docs/env.html>`_
    so you have working references and proper formatting.


.. module:: plone

.. _chapter_relation:

=========
Relations
=========


.. _relation_get_example:

Get relations
=============

.. code-block:: python

    api.relation.get(source=source, target=target, relationship="friend", unrestricted=False, as_dict=False)

You must provide either source, target or relationship, or a combination of those.
``unrestricted`` and ``as_dict`` are optional.

By default the result is a list of ``RelationValue`` objects.

If you set ``as_dict=True`` it will return a dictionary with the names of the relations as keys and lists of objects as values.

By default the View permission is checked on the relation objects.
You only get objects that you are allowed to see.
Use the ``unrestricted`` parameter if you want to bypass this check.

To get back relations, so relations pointing to an item, use:

.. code-block:: python

    api.relation.get(target=target)

To get the objects connected by relations you can use the api of these return values:

.. code-block:: python

    for relation in api.relation.get(source=source):
        source = relation.from_object
        target = relation.to_object
        relationship = relation.from_attribute


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

If the relation is based on a ``RelationChoice`` or ``RelationList`` field on the source object, the value of that field is created/updated accordingly.


.. _relation_delete_example:

Delete relation
===============

Delete one or more relations:

.. code-block:: python

    api.relation.delete(source=source, target=target, relationship="friend")

In order to delete relation(s), you must provide either ``source``, ``target`` or ``relationship``.
You can mix and match.

Delete all relations from source to any target:

.. code-block:: python

    api.relation.delete(source=source)

Delete all relations from any source to this target:

.. code-block:: python

    api.relation.delete(target=target)

Delete relations with name "friend" from source to any target:

.. code-block:: python

    api.relation.delete(source=source, relationship="friend")

Delete relations with name "uncle" from any source to this target:

.. code-block:: python

    api.relation.delete(target=target, relationship="uncle")

Delete relations with name "enemy" from any source to any target:

.. code-block:: python

    api.relation.delete(relationship="enemy")

If a deleted relation is based on a ``RelationChoice`` or ``RelationList`` field on the source object, the value of the field is removed/updated accordingly.


Further reading
===============

For more information on possible flags and usage options please see the full :ref:`plone-api-relation` specification.
For more information on relations read the relevant `chapter in the Mastering Plone training <https://training.plone.org/5/mastering-plone/relations.html>`_.
