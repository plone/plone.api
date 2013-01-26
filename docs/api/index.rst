.. line-block::

    WARNING: If you are reading this on GitHub, DON'T! Read it on ReadTheDocs:
    http://ploneapi.readthedocs.org/en/latest/api.html so you have working
    references and proper formatting.


.. currentmodule:: plone

List of all API methods with descriptions
=========================================

api.portal
----------

.. autosummary::

    api.portal.get
    api.portal.get_navigation_root
    api.portal.get_tool
    api.portal.get_localized_time
    api.portal.send_email
    api.portal.show_message
    api.portal.get_registry_record


api.content
-----------

.. autosummary::

    api.content.get
    api.content.create
    api.content.delete
    api.content.copy
    api.content.move
    api.content.rename
    api.content.get_uuid
    api.content.get_state
    api.content.transition
    api.content.get_view


api.user
--------

.. autosummary::

    api.user.get
    api.user.create
    api.user.delete
    api.user.get_current
    api.user.is_anonymous
    api.user.get_users
    api.user.get_roles
    api.user.get_permissions
    api.user.grant_roles
    api.user.revoke_roles


api.group
---------

.. autosummary::

    api.group.get
    api.group.create
    api.group.delete
    api.group.add_user
    api.group.remove_user
    api.group.get_groups
    api.group.get_roles
    api.group.grant_roles
    api.group.revoke_roles


api.env
---------

.. autosummary::

    api.env.adopt_roles


Exceptions and errors
---------------------

.. autosummary::

    api.exc.PloneApiError
    api.exc.MissingParameterError
    api.exc.InvalidParameterError
    api.exc.CannotGetPortalError

