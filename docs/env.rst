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

Further reading
---------------

For more information on possible flags and usage options please see the full
:ref:`plone-api-env` specification.

