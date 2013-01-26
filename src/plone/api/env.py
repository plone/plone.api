from AccessControl.SecurityManagement import getSecurityManager
from contextlib import contextmanager
from plone.api.exc import InvalidParameterError
from plone.api.validation import required_parameters


@required_parameters('roles')
def adopt_roles(roles=None):
    """Context manager for temporarily switching roles.

    :param roles: New roles to gain inside block. Existing roles will be lost.
    :type roles: list of strings
    """
    if isinstance(roles, basestring):
        roles = [roles]

    if not roles:
        raise InvalidParameterError("Can't set an empty set of roles.")

    return _adopt_roles(roles)


@contextmanager
def _adopt_roles(roles):
    overriding_context = _GlobalRoleOverridingContext(roles)

    sm = getSecurityManager()
    sm.addContext(overriding_context)

    yield

    sm.removeContext(overriding_context)


class _GlobalRoleOverridingContext(object):
    # SecurityManager uses getOwner() and getWrappedOwner()
    # to work out which contexts to apply _proxy_roles in.
    # If they both return None, then _proxy_roles apply everywhere.
    def getOwner(self):
        return None

    def getWrappedOwner(self):
        return None

    def __init__(self, roles):
        self._proxy_roles = roles
