from zope.app.component.hooks import getSite
from zope.globalrequest import getRequest


def get_site():
    """ Return the Plone Site object. """
    return getSite()


def get_request():
    """ Return the current request. """
    return getRequest()
