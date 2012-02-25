from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite
from zope.globalrequest import getRequest

import random
import string


def get_site():
    """ Return the Plone Site object. """
    return getSite()


def get_request():
    """ Return the current request. """
    return getRequest()


def create_user(username, email, password=None, **kwargs):
    """Create user"""
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
