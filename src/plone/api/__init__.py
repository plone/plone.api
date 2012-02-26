from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFPlone.utils import getToolByName
from zope.app.component.hooks import getSite
from zope.component import getUtility
from zope.globalrequest import getRequest

import random
import string


def get_site():
    """Get the Plone Site object out of thin air without importing fancy
    Interfaces and doing multi adapter lookups.

    :returns: Plone Site object
    """
    return getSite()


def get_request():
    """Get the current request object out of thin air without importing fancy
    Interfaces and doing multi adapter lookups.

    :returns: Request object
    """
    return getRequest()


def get_tool(name=None, *args):
    """Get a portal tool in a simple way.

    :param email: [required] Name of the tool you want.
    :type email: string
    :returns: portal tool
    """
    if args:
        raise ValueError('Positional arguments are not allowed!')

    if not name:
        raise ValueError

    site = get_site()
    return getToolByName(site, name)
