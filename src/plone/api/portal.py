# -*- coding: utf-8 -*-
"""Module that provides various utility methods on the portal level."""

from Acquisition import aq_inner
from email.utils import formataddr
from email.utils import parseaddr
from plone.api.exc import CannotGetPortalError
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.globalrequest import getRequest


def get():
    """Get the Plone portal object out of thin air.

    Without the need to import fancy Interfaces and doing multi adapter lookups.

    :returns: Plone portal object
    :rtype: Portal object
    :Example: :ref:`portal_get_example`

    """
    portal = getSite()
    if portal:
        return portal
    raise CannotGetPortalError(
        "Unable to get the portal object. More info on "
        "http://ploneapi.readthedocs.org/en/latest/api.html"
        "#plone.api.exc.CannotGetPortalError")


def get_navigation_root(context=None):
    """Get the navigation root object for the context.

    This traverses the path up and returns the nearest navigation root.
    Useful for multi-lingual installations and sites with subsites.

    :param context: [required] Context on which to get the navigation root.
    :type context: context object
    :returns: Navigation Root
    :rtype: Portal object
    :Example: :ref:`portal_get_navigation_root_example`

    """
    if not context:
        raise ValueError("Missing required object: context")
    context = aq_inner(context)
    return getNavigationRootObject(context, get())


def get_tool(name=None):
    """Get a portal tool in a simple way.

    :param name: [required] Name of the tool you want.
    :type name: string
    :returns: The tool that was found by name
    :raises:
        :class:`~plone.api.exc.MissingParameterError`,
        :class:`~plone.api.exc.InvalidParameterError`
    :Example: :ref:`portal_get_tool_example`

    """
    if not name:
        raise MissingParameterError("Missing required parameter: name")

    try:
        return getToolByName(get(), name)
    except AttributeError:

        # get a list of all tools to display their names in the error msg
        portal = get()
        tools = []
        for id in portal.objectIds():
            if id.startswith('portal_'):
                tools.append(id)

        raise InvalidParameterError(
            "Cannot find a tool with name '%s'. \n"
            "Available tools are:\n"
            "%s" % (name, '\n'.join(tools)))


def send_email(sender=None, recipient=None, subject=None, body=None):
    """Send an email.

    :param sender: Email sender, 'from' field. If not set, the portal default
        will be used.
    :type sender: string
    :param recipient: [required] Email recipient, 'to' field.
    :type recipient: string
    :param subject: [required] Subject of the email.
    :type subject: string
    :param body: [required] Body text of the email
    :type body: string
    :raises:
        ValueError
    :Example: :ref:`portal_send_email_example`

    """
    if not recipient or not subject or not body:
        raise ValueError

    portal = get()
    ctrlOverview = getMultiAdapter((portal, portal.REQUEST),
                                   name='overview-controlpanel')
    if ctrlOverview.mailhost_warning():
        raise ValueError('MailHost is not configured.')

    encoding = portal.getProperty('email_charset', 'utf-8')

    if not sender:
        from_address = portal.getProperty('email_from_address', '')
        from_name = portal.getProperty('email_from_name', '')
        sender = formataddr((from_name, from_address))
        if parseaddr(sender)[1] != from_address:
            # formataddr probably got confused by special characters.
            sender = from_address

    # If the mail headers are not properly encoded we need to extract
    # them and let MailHost manage the encoding.
    if isinstance(body, unicode):
        body = body.encode(encoding)

    host = getToolByName(portal, 'MailHost')
    host.send(
        body,
        recipient,
        sender,
        subject=subject,
        charset=encoding,
        immediate=True
    )


def get_localized_time(datetime=None, long_format=False, time_only=False):
    """Display a date/time in a user-friendly way.

    It should be localized to the user's preferred language.

    Note that you can specify both long_format and time_only as True
    (or any other value that can be converted to a boolean True
    value), but time_only then wins: the long_format value is ignored.

    :param datetime: [required] Message to show.
    :type datetime: DateTime
    :param long_format: When true, show long date format. When false
        (default), show the short date format.
    :type long_format: boolean
    :param time_only: When true, show only the time, when false
        (default), show the date.
    :type time_only: boolean
    :returns: Localized time
    :rtype: string
    :raises:
        ValueError
    :Example: :ref:`portal_get_localized_time_example`

    """
    if not datetime:
        raise ValueError

    tool = get_tool(name='translation_service')
    request = getRequest()
    return tool.ulocalized_time(datetime, long_format, time_only,
                                domain='plonelocales', request=request)


def show_message(message=None, request=None, type='info'):
    """Display a status message.

    :param message: [required] Message to show.
    :type message: string
    :param request: [required] Request.
    :type request: TODO: hm?
    :param type: Message type. Possible values: 'info', 'warn', 'error'
    :type type: string
    :raises:
        ValueError
    :Example: :ref:`portal_show_message_example`

    """
    if not message:
        raise ValueError

    if not request:
        raise ValueError

    IStatusMessage(request).add(message, type=type)


def get_registry_record(name=None):
    """Get a record value from a the ``plone.app.registry``

    :param name: [required] Name
    :type name: string
    :returns: Registry record value
    :rtype: plone.app.registry registry record
    :Example: :ref:`portal_get_registry_record_example`
    """
    if not name:
        raise MissingParameterError("Missing required parameter: name")
    registry = getUtility(IRegistry)
    if isinstance(name, str):
        record = registry.get(name)
        if record is None:
            raise KeyError(u"'%s' is no existing record" % name)
        else:
            return record
    raise InvalidParameterError(u"The parameter has to be a string")


def set_registry_record(name=None, value=None):
    """Set a record value in the ``plone.app.registry``

    :param name: [required] Name of the record
    :type name: string
    :param value: [required] Value to set
    :type value: python primitive
    :Example: :ref:`portal_set_registry_value_example`
    """
    if not name:
        raise MissingParameterError(u"Missing required parameter: name")
    if value is None:
        raise MissingParameterError(u"Missing required parameter: value")
    if not isinstance(name, str):
        raise InvalidParameterError(u"The parameter 'name' has to be a string")
    registry = getUtility(IRegistry)
    if isinstance(name, str):
        registry[name] = value
