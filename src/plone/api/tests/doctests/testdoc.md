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
self.assertEqual(obj.id, 'my-content')
self.assertEqual(portal['my-content'].id, 'my-content')
```

Check in another code block:

```python
# self.assertEqual(obj.id, 'my-content')
self.assertEqual(api.content.get(path='/my-content').id, 'my-content')
self.assertEqual(portal['my-content'].id, 'my-content')
```
