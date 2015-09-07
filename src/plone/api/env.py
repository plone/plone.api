# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from contextlib import contextmanager
from pkg_resources import get_distribution
from plone.api import portal
from plone.api.exc import InvalidParameterError
from plone.api.exc import UserNotFoundError
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters
from zope.globalrequest import getRequest

import Globals
import traceback

IS_TEST = None


@at_least_one_of('username', 'user')
@mutually_exclusive_parameters('username', 'user')
def adopt_user(username=None, user=None):
    """Context manager for temporarily switching user inside a block.

    :param user: User object to switch to inside block.
    :type user: user object from acl_users.getUser() or api.user.get().
    :param username: username of user to switch to inside block.
    :type username: string
    :Example: :ref:`env_adopt_user_example`
    """
    # Grab the user object out of acl_users because this function
    # accepts 'user' objects that are actually things like MemberData
    # objects, which AccessControl isn't so keen on.

    unwrapped = None
    plone = portal.get()
    acls = [plone.acl_users, plone.__parent__.acl_users]

    if username is None:
        for acl_users in acls:
            unwrapped = acl_users.getUserById(user.getId())
            if unwrapped:
                break
    else:
        for acl_users in acls:
            unwrapped = acl_users.getUser(username)
            if unwrapped:
                break

    if unwrapped is None:
        raise UserNotFoundError

    # ZopeSecurityPolicy appears to strongly expect the user object to
    # be Acquisition-wrapped in the acl_users from which it was taken.
    user = unwrapped.__of__(acl_users)

    return _adopt_user(user)


@contextmanager
def _adopt_user(user):
    # Fortunately, AccessControl makes this fairly easy.

    # One reference to the current user is held by the security
    # manager's pet SecurityContext object (defined for both the C and
    # Python implementations in AccessControl/SecurityManagement.py).

    # Use getSecurityManager() to take a reference to the existing
    # security manager object. Use newSecurityManager() to replace it
    # with a new one whose context refers to the new user object.
    # Run the block, then put the original security manager back.

    old_security_manager = getSecurityManager()
    newSecurityManager(getRequest(), user)

    yield

    setSecurityManager(old_security_manager)


@required_parameters('roles')
def adopt_roles(roles=None):
    """Context manager for temporarily switching roles.

    :param roles: New roles to gain inside block. Existing roles will be lost.
    :type roles: list of strings
    :Example: :ref:`env_adopt_roles_example`
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


def debug_mode():
    """Returns True if your zope instance is running in debug mode.

    :Example: :ref:`env_debug_mode_example`
    """
    return Globals.DevelopmentMode


def test_mode():
    """Returns True if you are running the zope test runner.

    :Example: :ref:`env_test_mode_example`
    """
    global IS_TEST

    if IS_TEST is None:
        IS_TEST = False
        for frame in traceback.extract_stack():
            if 'testrunner' in frame[0] or 'testreport/runner' in frame[0]:
                IS_TEST = True
                break

    return IS_TEST


def plone_version():
    """Return Plone version number.

    :returns: string denoting what release of Plone this distribution contains
    :Example: :ref:`env_plone_version_example`
    """
    return get_distribution('Products.CMFPlone').version


def zope_version():
    """Return Zope 2 version number.

    :returns: string denoting what release of Zope2 this distribution contains
    :Example: :ref:`env_zope_version_example`
    """
    return get_distribution('Zope2').version
