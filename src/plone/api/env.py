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
    # Okay, this is fun. Start by reading AccessControl/interfaces.py

    # ISecurityManager has a pair of methods addContext and removeContext,
    # which are used here surrounding the block ("yield" in @contextmanager
    # executes the body of the "with" block).

    # addContext/removeContext add/pop items from a stack of security_contexts
    # Only the uppermost object in the stack is consulted during any given
    # permission check.

    # If the stack is empty, the default security policy gets used.
    overriding_context = _GlobalRoleOverridingContext(roles)

    sm = getSecurityManager()
    sm.addContext(overriding_context)

    yield

    sm.removeContext(overriding_context)


class _GlobalRoleOverridingContext(object):
    # ZopeSecurityPolicy will use security_context._proxy_roles in place of
    # the roles that would normally be active, provided that it happens to
    # consider the security_context object to be relevant.

    def __init__(self, roles):
        self._proxy_roles = roles

    # ZopeSecurityPolicy decides if a security context is relevant as follows:

    # permission = name of the relevant permission, e.g. "View".
    # object = object on which the permission is checked, e.g. the portal.
    # context = a AccessControl.SecurityManagement.SecurityContext() object.
    #     Refers to the current user object and the stack of security_contexts.
    # security_context = last object to have been added using
    #     SecurityManager.addContext(). Not at all the same as SecurityContext!
    # roles = the roles that are allowed to run permission on object.

    # If the security policy is "ownerous" (True by default. The mechanism
    # for turning it off is not documented and you REALLY DON'T
    # WANT TO ANYWAY, trust me):
    # owner = security_context.getOwner() # is called

    # If owner is not None, owner.allowed(object, roles) is called. If
    # that returns a false value, permission is immediately denied.

    # Next, if the security_context has a _proxy_roles object
    # attribute and bool(security_context._proxy_roles) is True,
    # wrapped = security_context.getWrappedOwner() # is called.

    # If wrapped is Acquisition-wrapped and wrapped._check_context(object)
    # returns a false value, permission is immediately denied.
    # Otherwise, permission will be granted if and only if there is at least
    # one common value between roles and proxy_roles.

    # Otherwise... context.user.allowed(object, roles) is called. Permission
    # is granted if that returns a true value, denied otherwise.

    # TL;DR: if you getSecurityManager().addContext(obj), and:
    # obj.getOwner() returns None, and:
    # obj.getWrappedOwner() returns None, and:
    # bool(obj._proxy_roles) is True, then:
    # obj will always be considered relevant, and obj._proxy_roles gets used
    # in place of whatever would normally be the roles-in-context here.

    # Yay!

    def getOwner(self):
        return None

    def getWrappedOwner(self):
        return None
