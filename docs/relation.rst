.. admonition:: GitHub-only

    WARNING: If you are reading this on GitHub, DON'T!
    Read the documentation at `docs.plone.org <http://docs.plone.org/develop/plone.api/docs/env.html>`_
    so you have working references and proper formatting.


.. module:: plone

.. _chapter_relation:

=========
Relations
=========

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


Get relations
=============

.. code-block:: python

    api.relation.get(source=source, target=target, relationship="friend", unrestricted=False, as_dict=False)

You must provide either source, target or relationship, ``unrestricted`` and ``as_dict`` are optional.

Use the ``as_dict`` parameter if you want the result to be returned as a dictionary.
Use the ``unrestricted`` parameter if you want to bypass the View permission check.

By default it returns a list.
If source, target and relationship are all given, returns a list with a single item.

To get back relations, so relations pointing to an item, use:

.. code-block:: python

    api.relation.get(target=target)


Further reading
===============

For more information on possible flags and usage options please see the full :ref:`plone-api-relation` specification.
