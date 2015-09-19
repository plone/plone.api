# -*- coding: utf-8 -*-
"""Module that provides various utility methods on the portal level."""

from Acquisition import aq_inner
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from datetime import date
from datetime import datetime as dtime
from email.utils import formataddr
from email.utils import parseaddr
from logging import getLogger
from plone.api.exc import CannotGetPortalError
from plone.api.exc import InvalidParameterError
from plone.api.validation import required_parameters
from plone.app.layout.navigation.root import getNavigationRootObject
from zope.component import getUtility
from zope.component import providedBy
from zope.component.hooks import getSite
from zope.globalrequest import getRequest

import pkg_resources

logger = getLogger('plone.api.portal')

try:
    pkg_resources.get_distribution('plone.registry')
    from plone.registry.interfaces import IRegistry
except pkg_resources.DistributionNotFound:
    logger.warning(
        'plone.registry is not installed. get_registry_record and '
        'set_registry_record will be unavailable.'
    )

try:
    pkg_resources.get_distribution('Products.PrintingMailHost')
except pkg_resources.DistributionNotFound:
    PRINTINGMAILHOST_ENABLED = False
else:
    # PrintingMailHost only patches in debug mode.
    # plone.api.env.debug_mode cannot be used here, because .env imports this
    # file
    import Globals
    PRINTINGMAILHOST_ENABLED = Globals.DevelopmentMode


def get():
    """Get the Plone portal object out of thin air.

    Without the need to import fancy Interfaces and doing multi adapter
    lookups.

    :returns: Plone portal object
    :rtype: Portal object
    :Example: :ref:`portal_get_example`
    """

    closest_site = getSite()
    if closest_site is not None:
        for potential_portal in closest_site.aq_chain:
            if ISiteRoot in providedBy(potential_portal):
                return potential_portal

    raise CannotGetPortalError(
        "Unable to get the portal object. More info on "
        "https://ploneapi.readthedocs.org/en/latest/api/exceptions.html"
        "#plone.api.exc.CannotGetPortalError"
    )


@required_parameters('context')
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
    context = aq_inner(context)
    return getNavigationRootObject(context, get())


@required_parameters('name')
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
            "Cannot find a tool with name '{0}'.\n"
            "Available tools are:\n"
            "{1}".format(name, '\n'.join(tools))
        )


@required_parameters('recipient', 'subject', 'body')
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
    portal = get()

    if not PRINTINGMAILHOST_ENABLED:
        from plone.api import content
        ctrlOverview = content.get_view(
            context=portal,
            request=portal.REQUEST,
            name='overview-controlpanel',
        )
        if ctrlOverview.mailhost_warning():
            raise ValueError('MailHost is not configured.')

    try:
        encoding = get_registry_record('plone.email_charset')
    except InvalidParameterError:
        encoding = portal.getProperty('email_charset', 'utf-8')

    if not sender:
        try:
            from_address = get_registry_record('plone.email_from_address')
            from_name = get_registry_record('plone.email_from_name')
        except InvalidParameterError:
            # Before Plone 5.0b2 these were stored in portal_properties
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

    host = get_tool('MailHost')
    host.send(
        body,
        recipient,
        sender,
        subject=subject,
        charset=encoding,
        immediate=True
    )


@required_parameters('datetime')
def get_localized_time(datetime=None, long_format=False, time_only=False):
    """Display a date/time in a user-friendly way.

    It should be localized to the user's preferred language.

    Note that you can specify both long_format and time_only as True
    (or any other value that can be converted to a boolean True
    value), but time_only then wins: the long_format value is ignored.

    You can also use datetime.datetime or datetime.date instead of Plone's
    DateTime. In case of datetime.datetime everything works the same, in
    case of datetime.date the long_format parameter is ignored and on time_only
    an empty string is returned.

    :param datetime: [required] Message to show.
    :type datetime: DateTime, datetime or date
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
    tool = get_tool(name='translation_service')
    request = getRequest()

    # isinstance won't work because of date -> datetime inheritance
    if type(datetime) is date:
        if time_only:
            return ''
        datetime = dtime(datetime.year, datetime.month, datetime.day)
        long_format = False

    return tool.ulocalized_time(
        datetime,
        long_format,
        time_only,
        domain='plonelocales',
        request=request,
    )


@required_parameters('message', 'request')
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
    IStatusMessage(request).add(message, type=type)


@required_parameters('name')
def get_registry_record(name=None):
    """Get a record value from a the ``plone.app.registry``

    :param name: [required] Name
    :type name: string
    :returns: Registry record value
    :rtype: plone.app.registry registry record
    :Example: :ref:`portal_get_registry_record_example`
    """
    if not isinstance(name, str):
        raise InvalidParameterError(u"The parameter has to be a string")

    registry = getUtility(IRegistry)
    if name not in registry:
        # Show all records that 'look like' name.
        # We don't dump the whole list, because it 1500+ items.
        records = [key for key in registry.records.keys() if name in key]
        if records:
            raise InvalidParameterError(
                "Cannot find a record with name '{0}'.\n"
                "Did you mean?:\n"
                "{1}".format(name, '\n'.join(records))
            )
        else:
            raise InvalidParameterError(
                "Cannot find a record with name '{0}'".format(name)
            )

    return registry[name]


@required_parameters('name', 'value')
def set_registry_record(name=None, value=None):
    """Set a record value in the ``plone.app.registry``

    :param name: [required] Name of the record
    :type name: string
    :param value: [required] Value to set
    :type value: python primitive
    :Example: :ref:`portal_set_registry_record_example`
    """
    if not isinstance(name, str):
        raise InvalidParameterError(u"The parameter 'name' has to be a string")
    registry = getUtility(IRegistry)
    if isinstance(name, str):

        # confirm that the record exists before setting the value
        get_registry_record(name)

        registry[name] = value
