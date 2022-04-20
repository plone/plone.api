```{eval-rst}
.. module:: plone
    :noindex:
```


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
self.assertEqual(obj.title, 'My Content')
self.assertEqual(obj.id, 'my-content')
```

Nullam id dolor id nibh ultricies vehicula ut id elit. Praesent commodo cursus magna, vel scelerisque nisl consectetur et.

```python
# let's first get the portal object
from plone import api
portal = api.portal.get()
self.assertEqual(portal.id, 'plone')

# content can be accessed directly with dict-like access
myContent = portal['my-content']
self.assertEqual(myContent.title, 'My Content')

# another way is to use ``get()`` method and pass it a path
myContent = api.content.get(path='/my-content')
self.assertEqual(myContent.id, 'my-content')
```

Just for fun. The site has id 'plone'.

```python
# let's first get the portal object
from plone import api
portal = api.portal.get()
self.assertEqual(portal.id, 'plone')
```
