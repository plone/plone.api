# -*- coding: utf-8 -*-
"""Module that provides information on current context."""

from copy import copy as _copy
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution
from pkg_resources import parse_version
from plone.api import portal
from plone.api.exc import InvalidParameterError
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters
from plone.app.linkintegrity.exceptions import (
    LinkIntegrityNotificationException,
)  # noqa
from plone.app.uuid.utils import uuidToObject
from plone.uuid.interfaces import IUUID
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.container.interfaces import INameChooser
from zope.interface import Interface
from zope.interface import providedBy


def get_portal_state(context, request):
    return getMultiAdapter((context, request), name="plone_context_state")


@required_parameters("context", "request")
def view_template_id(context=None, request=None, **kwargs):  # NOQA: C816
    """The id of the view template of the context.

    :param context: [required] Context on which to get view.
    :type context: context object
    :param request: [required] Request on which to get view.
    :type request: request object
    :raises:
        :class:`~plone.api.exc.MissingParameterError`,
        :class:`~plone.api.exc.InvalidParameterError`
    :Example: :ref:`context_view_template_id_example`
    """
    pstate = get_portal_state(context, request)
    return pstate.view_template_id()


@required_parameters("context", "request")
def current_page_url(context=None, request=None, **kwargs):  # NOQA: C816
    """The URL to the current page, including template and query string.

    :param context: [required] Context on which to get view.
    :type context: context object
    :param request: [required] Request on which to get view.
    :type request: request object
    :raises:
        :class:`~plone.api.exc.MissingParameterError`,
        :class:`~plone.api.exc.InvalidParameterError`
    :Example: :ref:`context_current_page_url_example`
    """
    pstate = get_portal_state(context, request)
    return pstate.current_page_url()


@required_parameters("context", "request")
def current_base_url(context=None, request=None, **kwargs):  # NOQA: C816
    """The current "actual" URL from the request, excluding the query
string.

    :param context: [required] Context on which to get view.
    :type context: context object
    :param request: [required] Request on which to get view.
    :type request: request object
    :raises:
        :class:`~plone.api.exc.MissingParameterError`,
        :class:`~plone.api.exc.InvalidParameterError`
    :Example: :ref:`context_current_base_url_example`
    """
    pstate = get_portal_state(context, request)
    return pstate.current_base_url()