from email.utils import formataddr, parseaddr

from Products.CMFPlone.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from zope.app.component.hooks import getSite
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from plone.app.layout.navigation.root import getNavigationRoot

from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError
from plone.api.exc import CannotGetPortalError


def get():
    """Get the Plone portal object out of thin air without importing fancy
    Interfaces and doing multi adapter lookups.

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


def get_navigation_root():
    """Returns Plone's Navigation Root object. Useful in multi-lingual
    installations.

    :returns: Navigation Root
    :rtype: Portal object
    :Example: :ref:`portal_get_navigation_root_example`
    """
    return getNavigationRoot(get())


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

        # get a list of all tools so we can display their names in the error msg
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


def get_helpers():
    """Not yet implemented. Easy access to the ``@@plone_portal_state`` view.

    :returns: @@plone_portal_state view
    :rtype: BrowserView
    :Example: :ref:`portal_get_helpers_example`
    """
    raise NotImplementedError


def get_registry_record():
    """Not yet implemented. Easy access to the ``plone.app.registry`` configuration records.

    :returns: Registry record
    :rtype: plone.app.registry registry record
    :Example: :ref:`portal_get_helpers_example`
    """
    raise NotImplementedError
