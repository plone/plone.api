from zope.app.component.hooks import getSite


def get_site():
    """ Return the Plone Site object. """
    return getSite()
