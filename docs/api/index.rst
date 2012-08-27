.. line-block::

    WARNING: If you are reading this on GitHub, DON'T! Read it on ReadTheDocs:
    http://ploneapi.readthedocs.org/en/latest/api.html so you have working
    references and proper formatting.


.. currentmodule:: plone

Complete API
============

api.portal
----------

.. autosummary::

    api.portal.get
    api.portal.get_tool
    api.portal.url
    api.portal.get_tool
    api.portal.localized_time
    api.portal.send_email
    api.portal.show_message
    api.portal.url


api.content
-----------

.. autosummary::

    api.content.copy
    api.content.create
    api.content.delete
    api.content.get
    api.content.get_state
    api.content.get_view
    api.content.transition
    api.content.move


api.user
--------

.. autosummary::

    api.user.create
    api.user.delete
    api.user.get
    api.user.get_all
    api.user.get_current
    api.user.get_groups
    api.user.has_permission
    api.user.has_role
    api.user.is_anonymous


api.group
---------

.. autosummary::

    api.group.create
    api.group.add_user
    api.group.delete_user
    api.group.get
    api.group.get_all



Exceptions and errors
---------------------

.. autosummary::

    api.exceptions.PloneApiError
    api.exceptions.MissingParameterError
    api.exceptions.InvalidParameterError
    api.exceptions.CannotGetPortalError

