---
myst:
  html_meta:
    "description": "Get, modify, and delete content"
    "property=og:description": "Get, modify, and delete content"
    "property=og:title": "Content"
    "keywords": "Plone, API, development"
---

```{eval-rst}
.. currentmodule:: plone.api.content
```
% The Sphinx directive `currentmodule` is used to both run `code-block` examples via [Manuel](https://manuel.readthedocs.io/en/latest/#code-blocks-1) and to avoid duplicating an index entry that is already provided by its counterpart in `docs/api/*.md`.


(chapter-content)=

# Content

(content-create-example)=

## Create content

To add an object, you must first have a container to put it in.
Get the portal object; it will serve nicely:

```python
from plone import api
portal = api.portal.get()
```

Create your new content item using the {meth}`api.content.create` method.
The type argument will decide which content type will be created.

```python
from plone import api
obj = api.content.create(
    type='Document',
    title='My Content',
    container=portal)
```

The `id` of the new object is automatically and safely generated from its `title`.

```python
self.assertEqual(obj.id, 'my-content')
```

(content-get-example)=

## Get content object

There are several approaches to getting your content object.
Consider the following portal structure:

```console
plone (portal root)
├── blog
├── about
│   ├── team
│   └── contact
└── events
    ├── training
    ├── conference
    └── sprint
```

% invisible-code-block: python
%
% portal = api.portal.get()
% image = api.content.create(type='Image', id='image', container=portal)
% blog = api.content.create(type='Link', id='blog', container=portal)
% about = api.content.create(type='Folder', id='about', container=portal)
% events = api.content.create(type='Folder', id='events', container=portal)
%
% api.content.create(container=about, type='Document', id='team')
% api.content.create(container=about, type='Document', id='contact')
%
% api.content.create(container=events, type='Event', id='training')
% api.content.create(container=events, type='Event', id='conference')
% api.content.create(container=events, type='Event', id='sprint')

The following operations will get objects from the structure above, using {meth}`api.content.get`.

```python
# let's first get the portal object
from plone import api
portal = api.portal.get()
assert portal.id == 'plone'

# content can be accessed directly with dict-like access
blog = portal['blog']

# another way is to use ``get()`` method and pass it a path
about = api.content.get(path='/about')

# more examples
conference = portal['events']['conference']
sprint = api.content.get(path='/events/sprint')

# moreover, you can access content by its UID
uid = about['team'].UID()
team = api.content.get(UID=uid)

# returns None if UID cannot be found in catalog
not_found = api.content.get(UID='notfound')
```

% invisible-code-block: python
%
% self.assertTrue(portal)
% self.assertTrue(blog)
% self.assertTrue(about)
% self.assertTrue(conference)
% self.assertTrue(sprint)
% self.assertTrue(team)
% self.assertEqual(not_found, None)

(content-find-example)=

## Find content objects

You can use the {func}`api.content.find` function to search for content.

Finding all Documents:

```python
from plone import api
documents = api.content.find(portal_type='Document')
```

% invisible-code-block: python
%
% self.assertGreater(len(documents), 0)

Finding all Documents within a context:

```python
from plone import api
documents = api.content.find(
    context=api.portal.get(), portal_type='Document')
```

% invisible-code-block: python
%
% self.assertGreater(len(documents), 0)

Limit search depth:

```python
from plone import api
documents = api.content.find(depth=1, portal_type='Document')
```

% invisible-code-block: python
%
% self.assertGreater(len(documents), 0)

Limit search depth within a context:

```python
from plone import api
documents = api.content.find(
    context=api.portal.get(), depth=1, portal_type='Document')
```

% invisible-code-block: python
%
% self.assertGreater(len(documents), 0)

Search by interface:

```python
from plone import api
from Products.CMFCore.interfaces import IContentish
documents = api.content.find(object_provides=IContentish)
```

% invisible-code-block: python
%
% self.assertGreater(len(documents), 0)

Combining multiple arguments:

```python
from plone import api
from Products.CMFCore.interfaces import IContentish
documents = api.content.find(
    context=api.portal.get(),
    depth=2,
    object_provides=IContentish,
    SearchableText='Team',
)
```

% invisible-code-block: python
%
% self.assertGreater(len(documents), 0)

Find all `Document` content types, and use unrestricted search results:

```python
from plone import api
documents = api.content.find(
    context=api.portal.get(),
    portal_type="Document",
    unrestricted=True,
)
```

% invisible-code-block: python
%
% self.assertGreater(len(documents), 0)

More information about how to use the catalog may be found in the
[Plone Documentation](https://5.docs.plone.org/develop/plone/searching_and_indexing/index.html).

Note that the catalog returns *brains* (metadata stored in indexes) and not objects.
However, calling `getObject()` on brains does in fact give you the object.

```python
document_brain = documents[0]
document_obj = document_brain.getObject()
```

(content-get-uuid-example)=

## Get content object UUID

A Universally Unique IDentifier (UUID) is a unique, non-human-readable identifier for a content object which remains constant for the object even if the object is moved.

Plone uses UUIDs for storing references between content and for linking by UIDs, enabling persistent links.

To get the UUID of any content object use {meth}`api.content.get_uuid`.
The following code gets the UUID of the `contact` document.

```python
from plone import api
portal = api.portal.get()
contact = portal['about']['contact']

uuid = api.content.get_uuid(obj=contact)
```

% invisible-code-block: python
%
% self.assertTrue(isinstance(uuid, str))

(content-move-example)=

## Move content

To move content around the portal structure defined above use the {meth}`api.content.move` method.
The code below moves the `contact` item (with all it contains) out of the folder `about` and into the Plone portal root.

```python
from plone import api
portal = api.portal.get()
contact = portal['about']['contact']

api.content.move(source=contact, target=portal)
```

% invisible-code-block: python
%
% self.assertFalse(portal['about'].get('contact'))
% self.assertTrue(portal['contact'])

Actually, `move` behaves like a filesystem move.
If you pass it an `id` argument, the object will have that new ID in its new home.
By default it will retain its original ID.

% invisible-code-block: python
%
% self.assertEqual(contact.id, "contact")
% self.assertTrue(portal['contact'])
% contact = portal['contact']
% api.content.move(source=contact, target=portal['about'], id="new-contact")
% self.assertEqual(contact.id, "new-contact")
% self.assertTrue(portal['about']['new-contact'])

(content-rename-example)=

## Rename content

To rename a content object (change its ID), use the {meth}`api.content.rename` method.

```python
from plone import api
portal = api.portal.get()
api.content.rename(obj=portal['blog'], new_id='old-blog')
```

% invisible-code-block: python
%
% self.assertFalse(portal.get('blog'))
% self.assertTrue(portal['old-blog'])

(content-copy-example)=

## Copy content

To copy a content object, use the {meth}`api.content.copy` method.

```python
from plone import api
portal = api.portal.get()
training = portal['events']['training']

api.content.copy(source=training, target=portal)
```

Note that the new object will have the same ID as the old object (unless otherwise stated).
This is not a problem, since the new object is in a different container.

% invisible-code-block: python
%
% assert portal['events']['training'].id == 'training'
% assert portal['training'].id == 'training'

You can also set `target` to source's container and set `safe_id=True`.
This will duplicate your content object in the same container and assign it a new, non-conflicting ID.

```python
api.content.copy(source=portal['training'], target=portal, safe_id=True)
new_training = portal['copy_of_training']
```

% invisible-code-block: python
%
% self.assertTrue(portal['training'])  # old object remains
% self.assertTrue(portal['copy_of_training'])

(content-delete-example)=

## Delete content

To delete a content object, pass the object to the {meth}`api.content.delete` method:

```python
from plone import api
portal = api.portal.get()
api.content.delete(obj=portal['copy_of_training'])
```

% invisible-code-block: python
%
% self.assertFalse(portal.get('copy_of_training'))

To delete multiple content objects, pass the objects to the {meth}`api.content.delete` method:

% invisible-code-block: python
%
% api.content.copy(source=portal['training'], target=portal, safe_id=True)
% api.content.copy(source=portal['events']['training'], target=portal['events'], safe_id=True)

```python
from plone import api
portal = api.portal.get()
data = [portal['copy_of_training'], portal['events']['copy_of_training'], ]
api.content.delete(objects=data)
```

% invisible-code-block: python
%
% self.assertFalse(portal.get('copy_of_training'))
% self.assertFalse(portal.events.get('copy_of_training'))

If deleting content would result in broken links you will get a `LinkIntegrityNotificationException`. To delete anyway, set the option `check_linkintegrity` to `False`:

% invisible-code-block: python
%
% from plone.app.textfield import RichTextValue
% from zope.lifecycleevent import modified
% api.content.copy(source=portal['training'], target=portal, safe_id=True)
% api.content.copy(source=portal['events']['training'], target=portal['events'], safe_id=True)
% portal['about']['team'].text = RichTextValue('<a href="../copy_of_training">contact</a>', 'text/html', 'text/x-html-safe')
% modified(portal['about']['team'])

```python
from plone import api
portal = api.portal.get()
api.content.delete(obj=portal['copy_of_training'], check_linkintegrity=False)
```

% invisible-code-block: python
%
% self.assertNotIn('copy_of_training', portal.keys())

(content-manipulation-with-safe-id-option)=

## Content manipulation with the `safe_id` option

When you manipulate content with {meth}`api.content.create`, {meth}`api.content.move` or {meth}`api.content.copy` the `safe_id` flag is disabled by default.
This means the uniqueness of IDs will be enforced.
If another object with the same ID is already present in the target container these API methods will raise an error.

However, if the `safe_id` option is enabled, a non-conflicting ID will be generated.

% invisible-code-block: python
%
% api.content.create(container=portal, type='Document', id='document', safe_id=True)

```python
api.content.create(container=portal, type='Document', id='document', safe_id=True)
document = portal['document-1']
```

(content-get-state-example)=

## Get workflow state

To find out the current workflow state of your content, use the {meth}`api.content.get_state` method.

```python
from plone import api
portal = api.portal.get()
state = api.content.get_state(obj=portal['about'])
```

% invisible-code-block: python
%
% self.assertEqual(state, 'private')

The optional `default` argument is returned if no workflow is defined for the object.

```python
from plone import api
portal = api.portal.get()
state = api.content.get_state(obj=portal['image'], default='Unknown')
```

% invisible-code-block: python
%
% self.assertEqual(state, 'Unknown')

(content-transition-example)=

## Transition

To transition your content to a new workflow state, use the {meth}`api.content.transition` method.

```python
from plone import api
portal = api.portal.get()
api.content.transition(obj=portal['about'], transition='publish')
```

% invisible-code-block: python
%
% self.assertEqual(
%     api.content.get_state(obj=portal['about']),
%     'published'
% )

If your workflow accepts any additional arguments to the checkin method you may supply them via kwargs.
These arguments can be saved to your transition using custom workflow variables inside the ZMI using an expression such as "python:state_change.kwargs.get('comment', '')"

```python
from plone import api
portal = api.portal.get()
api.content.transition(obj=portal['about'], transition='reject', comment='You had a typo on your page.')
```

(content-disable-roles-acquisition-example)=

## Disable local roles acquisition

To disable the acquisition of local roles for an object, use the {meth}`api.content.disable_roles_acquisition` method.

```python
from plone import api
portal = api.portal.get()
api.content.disable_roles_acquisition(obj=portal['about'])
```

% invisible-code-block: python
%
% ac_flag = getattr(portal['about'], '__ac_local_roles_block__', None)
% self.assertTrue(ac_flag)

(content-enable-roles-acquisition-example)=

## Enable local roles acquisition

To enable the acquisition of local roles for an object, use the {meth}`api.content.enable_roles_acquisition` method.

```python
from plone import api
portal = api.portal.get()
api.content.enable_roles_acquisition(obj=portal['about'])
```

% invisible-code-block: python
%
% # As __ac_local_roles_block__ is None by default, we have to set it,
% # before we can test the enabling method.
% portal['about'].__ac_local_roles_block__ = 1
%
% api.content.enable_roles_acquisition(obj=portal['about'])
% ac_flag = getattr(portal['about'], '__ac_local_roles_block__', None)
% self.assertFalse(ac_flag)

(content-get-view-example)=

## Get view

To get a {class}`BrowserView` for your content, use {meth}`api.content.get_view`.

```python
from plone import api
portal = api.portal.get()
view = api.content.get_view(
    name='plone',
    context=portal['about'],
    request=request,
)
```

% invisible-code-block: python
%
% self.assertEqual(view.__name__, 'plone')

Since version `2.0.0`, the `request` argument can be omitted.
In that case, the global request will be used.

```python
from plone import api
portal = api.portal.get()
view = api.content.get_view(
    name='plone',
    context=portal['about'],
)
```

% invisible-code-block: python
%
% self.assertEqual(view.__name__, u'plone')

(content-get-path-example)=

## Get content path

To get the path of a content object, use {func}`api.content.get_path`.
This function accepts an object for which you want to get its path as the required parameter `obj`, and an optional boolean parameter `relative` whose default is `False`.

It returns either an absolute path from the Zope root by default or when `relative` is set to `False`, or a relative path from the portal root when `relative` is set to `True`.

The following example shows how to get the absolute path from the Zope root.

```python
from plone import api
portal = api.portal.get()

folder = portal["events"]["training"]
path = api.content.get_path(obj=folder)
assert path == "/plone/events/training"
```

The following example shows how to get the portal-relative path.

```python
rel_path = api.content.get_path(obj=folder, relative=True)
assert rel_path == "events/training"
```

If the API is used to fetch an object with the `relative` parameter set as `True`, and the object is outside the portal, it throws an `InvalidParameterError` error.

% invisible-code-block: python
%
% # Setup an object outside portal for testing error case
% app = portal.aq_parent
% app.manage_addFolder("outside_folder")
%
% # Test that getting relative path for object outside portal raises error
% from plone.api.exc import InvalidParameterError
% with self.assertRaises(InvalidParameterError):
%     api.content.get_path(obj=app.outside_folder, relative=True)

```python
from plone.api.exc import InvalidParameterError

# Getting path of an object outside portal raises InvalidParameterError
try:
    outside_path = api.content.get_path(
        obj=app.outside_folder,
        relative=True
    )
    assert False, "Should raise InvalidParameterError and not reach this code"
except InvalidParameterError as e:
    assert "Object not in portal path" in str(e)
```

(content-iter-ancestors-example)=

## Iterate over object ancestors

To iterate over the ancestors in the object tree, use the {func}`api.content.iter_ancestors` function.

```python
from plone import api
portal = api.portal.get()

# Get all ancestors of the team object
ancestors = api.content.iter_ancestors(portal.about.team)
```

% invisible-code-block: python
%
% self.assertTupleEqual(tuple(ancestors), (portal.about, portal))

To iterate over the ancestors that implement one interface, use the {func}`api.content.iter_ancestors` function with the `interface` argument.

```python
from plone import api
from Products.CMFCore.interfaces import ISiteRoot
portal = api.portal.get()

# Get all ancestors of the team object that implement the ISiteRoot interface
ancestors = api.content.iter_ancestors(portal.about.team, interface=ISiteRoot)
```

% invisible-code-block: python
%
% self.assertTupleEqual(tuple(ancestors), (portal,))

To iterate over the ancestors using a custom filter you can use the {func}`api.content.iter_ancestors` function with the `function` argument.

```python
from plone import api
portal = api.portal.get()

# Get all ancestors of the team object with the id 'about'
ancestors = api.content.iter_ancestors(portal.about.team, function=lambda obj: obj.id == "about")
```

% invisible-code-block: python
%
% self.assertTupleEqual(tuple(ancestors), (portal.about,))

To iterate over the ancestors until an object is found, use the {func}`api.content.iter_ancestors` function with the `stop_at` argument.

```python
from plone import api
portal = api.portal.get()

# Get all ancestors of the team object until the object 'about'
ancestors = api.content.iter_ancestors(portal.about.team, stop_at=portal.about)
```

% invisible-code-block: python
%
% self.assertTupleEqual(tuple(ancestors), (portal.about,))

(content-get-closest-ancestor-example)=

## Get closest ancestor

To get the closest ancestor in the object tree, use the {func}`api.content.get_closest_ancestor` function.

```python
from plone import api
from Products.CMFCore.interfaces import ISiteRoot
portal = api.portal.get()

# Get the closest ancestor of the team object that implements the ISiteRoot interface
ancestor = api.content.get_closest_ancestor(portal.about.team, interface=ISiteRoot)
```

% invisible-code-block: python
%
% self.assertEqual(ancestor, portal)

To get the closest ancestor by using a custom filter, use the {func}`api.content.get_closest_ancestor` function with the `function` argument.

```python
from plone import api
portal = api.portal.get()

# Get the closest ancestor of the team object with the id 'about'
ancestor = api.content.get_closest_ancestor(portal.about.team, function=lambda obj: obj.id == "about")
```

% invisible-code-block: python
%
% self.assertEqual(ancestor, portal.about)

## Further reading

For more information on possible flags and usage options please see the full {ref}`plone-api-content` specification.
