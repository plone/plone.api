.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T!
    Read the documentation at `docs.plone.org <http://docs.plone.org/develop/plone.api/docs/env.html>`_
    so you have working references and proper formatting.


.. module:: plone

.. _chapter_relation:

=========
Relations
=========

To use the relations code, you should include `plone.api[relations]` in the dependencies of your project.

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

Delete one specific relationship:

.. code-block:: python

    api.relation.delete(source=source, target=target, relationship="friend")

You can delete all relations by explicitly asking:

.. code-block:: python

    api.relation.delete(delete_all=True)

In all other cases, in order to delete relation(s), you must provide either ``source``, ``target`` or ``relationship``.
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
