from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SimpleObjectPolicies import _noroles
from contextlib import contextmanager
from plone.api.exc import InvalidParameterError
from plone.api.exc import MissingParameterError


class GlobalRoleOverridingContext(object):
    # SecurityManager uses getOwner() and getWrappedOwner()
    # to work out which contexts to apply _proxy_roles in.
    # If they both return None, then _proxy_roles apply everywhere.

    def getOwner(self):
        return None

    def getWrappedOwner(self):
        return None

    def __init__(self, roles):
        self._proxy_roles = roles
    #     self._poxy = roles

    # @property
    # def _proxy_roles(self):
    #     print ":", self._poxy
    #     return self._poxy


def roles(roles=None):
    """
    Context manager for temporarily switching roles.

    The supplied set of roles will replace the existing active roles.

    e.g.
    from AccessControl import Unauthorized
    from plone import api

    with api.adopt(roles=['Reviewer']):
        self.assertRaises(
            Unauthorized
            self.index
        )

    :param roles: New roles to gain inside block.
    :type roles: list of strings
    """
    if roles is None:
        raise MissingParameterError("roles")

    if isinstance(roles, basestring):
        roles = [roles]

    if not roles:
        raise InvalidParameterError("Can't set an empty set of roles.")

    return adopt_roles(roles)

@contextmanager
def adopt_roles(roles):
    overriding_context = GlobalRoleOverridingContext(roles)

    sm = getSecurityManager()
    sm.addContext(overriding_context)

    yield

    sm.removeContext(overriding_context)
