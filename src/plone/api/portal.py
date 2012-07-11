from Products.CMFPlone.utils import getToolByName
from zope.app.component.hooks import getSite


def get():
    """Get the Plone Site object out of thin air without importing fancy
    Interfaces and doing multi adapter lookups.

    :returns: Plone Site object
    :Example: :ref:`portal_get_example`
    """
    return getSite()


def url():
    """Get the site url.

    :returns: Site url
    :rtype: string
    :Example: :ref:`portal_url_example`
    """
    return getSite().absolute_url()


def get_tool(name=None, *args):
    """Get a portal tool in a simple way.

    :param email: [required] Name of the tool you want.
    :type email: string
    :returns: portal tool
    :Example: :ref:`portal_get_tool_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not name:
        raise ValueError

    return getToolByName(getSite(), name)


def send_email(sender=None, recipient=None, subject=None, body=None, *args):
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
    :Example: :ref:`portal_send_email_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not recipient or not subject or not body:
        raise ValueError

    portal = getSite()
    encoding = portal.getProperty('email_charset', 'utf-8')

    if not sender:
        sender = portal.getProperty('email_from_name') + \
            ' <' + portal.getProperty('email_from_address') + '>'

    # The mail headers are not properly encoded we need to extract
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


def localized_time(datetime=None, request=None, *args):
    raise NotImplementedError


def show_message(message=None, type='info', *args):
    """Display a status message.

    :param message: [required] Message to show.
    :type message: string
    :param type: Message type. Possible values: 'info', 'warn', 'error'
    :type type: string
    :Example: :ref:`show_message_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not message:
        raise ValueError

    raise NotImplementedError
