---
myst:
  html_meta:
    "description": "Create, access, modify, and delete groups and group memberships"
    "property=og:description": "Create, access, modify, and delete groups and group memberships"
    "property=og:title": "Groups"
    "keywords": "Plone, development, API, users, groups"
---

```{eval-rst}
.. currentmodule:: plone.api.group
```
% The Sphinx directive `currentmodule` is used to both run `code-block` examples via [Manuel](https://manuel.readthedocs.io/en/latest/#code-blocks-1) and to avoid duplicating an index entry that is already provided by its counterpart in `docs/api/*.md`.

(chapter-groups)=

# Groups

(group-create-example)=

## Create group

To create a new group, use {meth}`api.group.create`, providing a required string parameter of `groupname`.

```python
from plone import api
group = api.group.create(groupname='staff')
```

% invisible-code-block: python
%
% self.assertEqual(group.id, 'staff')

When you create groups, `title`, `description`, `roles` and `groups` are optional.

```python
from plone import api

group = api.group.create(
    groupname='board_members',
    title='Board members',
    description='Just a description',
    roles=['Reader', ],
    groups=['Site Administrators', ],
)
```

% invisible-code-block: python
%
% self.assertEqual(group.id, 'board_members')
% self.assertEqual(group.getProperty('title'), 'Board members')
% self.assertEqual(group.getProperty('description'), 'Just a description')
% self.assertTrue('Reader' in group.getRoles())
% self.assertTrue('Site Administrators' in group.getMemberIds())

(group-get-example)=

## Get group

To get a group by its name, use {meth}`api.group.get`.

```python
from plone import api
group = api.group.get(groupname='staff')
```

% invisible-code-block: python
%
% self.assertEqual(group.id, 'staff')

(group-edit-example)=

## Editing a group

Groups can be edited by using the method {meth}`api.portal.get_tool`, providing the portal tool `portal_groups` as the `name` argument.
In this example, the `title`, `description` and `roles` are updated for the group `staff`.

```python
from plone import api
portal_groups = api.portal.get_tool(name='portal_groups')
portal_groups.editGroup(
    'staff',
    roles=['Editor', 'Reader'],
    title='Staff',
    description='Just a description',
)
```

% invisible-code-block: python
%
% group = api.group.get(groupname='staff')
%
% title = group.getProperty('title')
% description = group.getProperty('description')
% roles = group.getRoles()
%
% self.assertEqual(title, 'Staff')
% self.assertEqual(description, 'Just a description')
% self.assertTrue('Editor' in roles)
% self.assertTrue('Reader' in roles)

(group-get-all-groups-example)=

## Get all groups

You can also get all groups by using {meth}`api.group.get_groups`.

```python
from plone import api
groups = api.group.get_groups()
```

% invisible-code-block: python
%
% self.assertEqual(groups[0].id, 'Administrators')

(group-get-users-groups-example)=

## Get user's groups

Groups may be filtered by member. By passing the `username` parameter,
{meth}`api.group.get_groups` will return only the groups the user belongs to.

% invisible-code-block: python
%
% api.user.create(email='jane@plone.org', username='jane')
% api.group.add_user(username='jane', groupname='staff')
% api.group.add_user(username='jane', groupname='Reviewers')

```python
from plone import api
groups = api.group.get_groups(username='jane')
```

% invisible-code-block: python
%
% group_list = [g.id for g in groups]
% self.assertCountEqual(
%     group_list,
%     ['Reviewers', 'AuthenticatedUsers', 'staff'],
% )

You can also pass the user directly to {meth}`api.group.get_groups`:

```python
from plone import api
user = api.user.get(username='jane')
groups = api.group.get_groups(user=user)
```

% invisible-code-block: python
%
% group_list = [g.id for g in groups]
% self.assertCountEqual(
%     group_list,
%     ['Reviewers', 'AuthenticatedUsers', 'staff'],
% )

## Get group members

Use the {meth}`api.user.get_users` method to get all the users that are members of a group.

```python
from plone import api
members = api.user.get_users(groupname='staff')
```

% invisible-code-block: python
%
% self.assertEqual(members[0].id, 'jane')

(group-delete-example)=

## Delete group

To delete a group, use {meth}`api.group.delete` and pass in either the groupname or the group object you want to delete.

```python
from plone import api
api.group.create(groupname='unwanted')
api.group.delete(groupname='unwanted')
```

% invisible-code-block: python
%
% self.assertEqual(api.group.get(groupname='unwanted'), None)

```python
unwanted = api.group.create(groupname='unwanted')
api.group.delete(group=unwanted)
```

% invisible-code-block: python
%
% self.assertEqual(api.group.get(groupname='unwanted'), None)

(group-add-user-example)=

## Adding user to group

To add a user to a group, use the {meth}`api.group.add_user` method.
This method accepts either the groupname or the group object for the target group and the username or the user object you want to add to the group.

```python
from plone import api

api.user.create(email='bob@plone.org', username='bob')
api.group.add_user(groupname='staff', username='bob')
```

% invisible-code-block: python
%
% self.assertTrue(
%     'staff' in [g.id for g in api.group.get_groups(username='bob')]
% )

(group-remove-user-example)=

## Removing user from group

To remove a user from a group, use the {meth}`api.group.remove_user` method.
This also accepts either the groupname or the group object for the target group and either the username or the user object you want to remove from the group.

```python
from plone import api
api.group.remove_user(groupname='staff', username='bob')
```

% invisible-code-block: python
%
% self.assertFalse('staff' in [g.id for g in api.group.get_groups(username='bob')])

(group-get-roles-example)=

## Get group roles

To find the roles assigned to a group, use the {meth}`api.group.get_roles` method.
By default it returns site-wide roles.

```python
from plone import api
roles = api.group.get_roles(groupname='staff')
```

% invisible-code-block: python
%
% EXPECTED_SITE_ROLES = ['Authenticated', 'Editor', 'Reader']
% self.assertEqual(set(EXPECTED_SITE_ROLES), set(roles))

If you pass in a content object, it will return the local roles of the group in that particular context.

```python
from plone import api
portal = api.portal.get()
folder = api.content.create(
    container=portal,
    type='Folder',
    id='folder_four',
    title='Folder Four',
)
roles = api.group.get_roles(groupname='staff', obj=portal['folder_four'])
```

% invisible-code-block: python
%
% self.assertEqual(set(EXPECTED_SITE_ROLES), set(roles))

If you pass in a content object and `inherit=False`, it will return only the local roles of the group on that particular object and ignore global roles.

```python
api.group.grant_roles(
    groupname='staff', roles=['Contributor'], obj=portal['folder_four'])

roles = api.group.get_roles(
    groupname='staff', obj=portal['folder_four'], inherit=False)
```

% invisible-code-block: python
%
% EXPECTED_OBJ_ROLES = ['Contributor']
% self.assertEqual(set(EXPECTED_OBJ_ROLES), set(roles))

(group-grant-roles-example)=

## Grant roles to group

To grant roles to a group, use the {meth}`api.group.grant_roles` method.
By default, roles are granted site-wide.

```python
from plone import api
api.group.grant_roles(
    groupname='staff',
    roles=['Reviewer, SiteAdministrator'],
)
```

% invisible-code-block: python
%
% EXPECTED_SITE_ROLES = ['Authenticated', 'Editor', 'Reader', 'Reviewer, SiteAdministrator']
% roles = api.group.get_roles(groupname='staff')
% self.assertEqual(set(EXPECTED_SITE_ROLES), set(roles))

If you pass in a content object, roles will be assigned in that particular context.

```python
from plone import api
portal = api.portal.get()
folder = api.content.create(
    container=portal, type='Folder', id='folder_five', title='Folder Five')
api.group.grant_roles(
    groupname='staff', roles=['Contributor'], obj=portal['folder_five'])
```

% invisible-code-block: python
%
% EXPECTED_CONTEXT_ROLES = EXPECTED_SITE_ROLES + ['Contributor']
% roles = api.group.get_roles(groupname='staff', obj=portal['folder_five'], inherit=False)
% self.assertEqual(set(['Contributor']), set(roles))
% roles = api.group.get_roles(groupname='staff', obj=portal['folder_five'])
% self.assertEqual(set(EXPECTED_CONTEXT_ROLES), set(roles))

(group-revoke-roles-example)=

## Revoke roles from group

To revoke roles already granted to a group, use the {meth}`api.group.revoke_roles` method.

```python
from plone import api
api.group.revoke_roles(
    groupname='staff', roles=['Reviewer, SiteAdministrator'])
```

% invisible-code-block: python
%
% EXPECTED_SITE_ROLES = ['Authenticated', 'Editor', 'Reader']
% roles = api.group.get_roles(groupname='staff')
% self.assertEqual(set(EXPECTED_SITE_ROLES), set(roles))

If you pass in a content object, it will revoke roles granted in that particular context.

% invisible-code-block: python
%
% EXPECTED_CONTEXT_ROLES = ['Contributor']
% roles = api.group.get_roles(groupname='staff', obj=portal['folder_five'], inherit=False)
% self.assertEqual(['Contributor'], roles)

```python
from plone import api
api.group.revoke_roles(
    groupname='staff', roles=['Contributor'], obj=portal['folder_five'])
```

% invisible-code-block: python
%
% EXPECTED_CONTEXT_ROLES = []
% roles = api.group.get_roles(groupname='staff', obj=portal['folder_five'], inherit=False)
% self.assertEqual(set(EXPECTED_CONTEXT_ROLES), set(roles))

## Further reading

For more information on possible flags and complete options please see the full {ref}`plone-api-group` specification.
