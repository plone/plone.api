# -*- coding: utf-8 -*-
"""Exceptions raised by plone.api methods."""


class PloneApiError(Exception):
    """Base exception class for plone.api errors."""


class MissingParameterError(PloneApiError):
    """Raised when a parameter is missing."""


class InvalidParameterError(PloneApiError):
    """Raised when a parameter is invalid."""


class CannotGetPortalError(PloneApiError):
    """Raised when the portal object cannot be retrieved.

    This normally happens if you are using plone.api ``bin/instance debug``,
    because debug sessions do not have a request and so the getSite() cannot
    know which Plone portal you want to get (as there can be multiple Plone
    sites).

    The solution is to use the ``-O <portal_id>`` parameter to tell Zope to
    traverse to a portal, for example ``bin/instance -O Plone debug.``
    """


class UserNotFoundError(PloneApiError):
    """Raised when a specified or implicit user can not be retrieved."""


class GroupNotFoundError(PloneApiError):
    """Raised when a specified or implicit group can not be retrieved."""
