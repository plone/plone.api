from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFPlone.utils import getToolByName
from zope.app.component.hooks import getSite
from zope.component import getUtility
from zope.globalrequest import getRequest

import random
import string


def get_site():
    """Return the Plone Site object."""
    return getSite()


def get_request():
    """Return the current request."""
    return getRequest()


def create(container, type, id, **kwargs):
    """Create content of the given type."""
    fti = get_site().portal_types[type]
    return fti.constructInstance(container, id, **kwargs)


def create_user(username, email, password=None, **kwargs):
    """Create user."""
    site = get_site()
    registration = getToolByName(site, 'portal_registration')

    # if password is not set, generate one
    if not password:
        random.seed()
        sample = random.sample(string.letters + string.digits, 8)
        password = ''.join(sample)

    # build user properties and add username into it
    properties = kwargs
    properties['username'] = username
    properties['email'] = email

    return registration.addMember(username, password, properties=properties)


def change_password(userid, password):
    """Change the user's password."""
    site = get_site()
    memberdata = getToolByName(site, 'portal_memberdata')
    member = memberdata.getMemberById(userid)
    member._setPassword(password)


def send_email(body="", recipient="", sender="", subject=""):
    """Send an email."""
    encoding = getUtility(ISiteRoot).getProperty('email_charset', 'utf-8')

    # The mail headers are not properly encoded we need to extract
    # them and let MailHost manage the encoding.
    if isinstance(body, unicode):
        body = body.encode(encoding)

    host = getToolByName(get_site(), 'MailHost')
    host.send(body, recipient, sender, subject=subject, charset=encoding,
              immediate=True)
