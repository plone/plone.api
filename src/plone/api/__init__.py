from Products.CMFPlone.utils import getToolByName
from zope.app.component.hooks import getSite
from zope.globalrequest import getRequest

# Magic imports for api modules
from plone.api import content, user, group


def get_site():
    """Get the Plone Site object out of thin air without importing fancy
    Interfaces and doing multi adapter lookups.

    :returns: Plone Site object
    :Example: :ref:`get_site_example`
    """
    return getSite()


def get_request():
    """Get the current request object out of thin air without importing fancy
    Interfaces and doing multi adapter lookups.

    :returns: Request object
    :Example: :ref:`get_request_example`
    """
    return getRequest()


def get_site_url():
    """Get the site url.

    :returns: Site url
    :rtype: string
    :Example: :ref:`get_site_url_example`
    """
    raise NotImplementedError


def show_message(message=None, mtype='info', *args):
    """Display a status message.

    :param message: [required] Message to show.
    :type message: string
    :param mtype: Message type. Possible values: 'info', 'warn', 'error'
    :type mtype: string
    :Example: :ref:`show_message_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not message:
        raise ValueError

    utils = get_tool('plone_utils')
    utils.addPortalMessage(message, mtype)


def get_tool(name=None, *args):
    """Get a portal tool in a simple way.

    :param email: [required] Name of the tool you want.
    :type email: string
    :returns: portal tool
    :Example: :ref:`get_tool_example`
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not name:
        raise ValueError

    site = get_site()
    return getToolByName(site, name)


def send_email(sender=None, recipient=None, subject=None, body=None, *args):
    """Send an email.

    :param sender: [required] Email sender, 'from' field.
    :type sender: string
    :param recipient: [required] Email recipient, 'to' field.
    :type recipient: string
    :param subject: [required] Subject of the email.
    :type subject: string
    :param body: [required] Body text of the email
    :type body: string
    :Example: :ref:`send_email_example`
    """

    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not sender or not recipient or not subject or not body:
        raise ValueError

    site = get_site()
    encoding = site.getProperty('email_charset', 'utf-8')

    # The mail headers are not properly encoded we need to extract
    # them and let MailHost manage the encoding.
    if isinstance(body, unicode):
        body = body.encode(encoding)

    host = getToolByName(get_site(), 'MailHost')
    host.send(
        body,
        recipient,
        sender,
        subject=subject,
        charset=encoding,
        immediate=True
    )
