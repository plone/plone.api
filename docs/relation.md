---
myst:
  html_meta:
    "description": "Create, access, modify, and delete relations of Plone content"
    "property=og:description": "Create, access, modify, and delete relations of Plone content"
    "property=og:title": "Relations"
    "keywords": "Plone, development, API, relations, related content"
---

```{eval-rst}
.. currentmodule:: plone.api.relation
```
% The Sphinx directive `currentmodule` is used to both run `code-block` examples via [Manuel](https://manuel.readthedocs.io/en/latest/#code-blocks-1) and to avoid duplicating an index entry that is already provided by its counterpart in `docs/api/*.md`.

(chapter-relation)=

# Relations


(relation-get-example)=

## Get relations

% invisible-code-block: python
%
% from plone import api
% portal = api.portal.get()
% bob = api.content.create(type='Document', id='bob', container=portal)
% bobby = api.content.create(type='Document', id='bobby', container=portal)
%
% source = bob
% target = bobby
% api.relation.create(source=source, target=target, relationship="friend")

```python
from plone import api

friendship = api.relation.get(
    source=source, target=target, relationship="friend", unrestricted=False, as_dict=False
    )
```

% invisible-code-block: python
%
% self.assertTrue(friendship)

You must provide either source, target, or relationship, or a combination of those, to {meth}`api.relation.get`.
`unrestricted` and `as_dict` are optional.

By default the result is a list of {class}`z3c.relationfield.RelationValue` objects.
If you set `as_dict=True` {meth}`api.relation.get` will return a dictionary with the names of the relations as keys and lists of objects as values.

By default the View permission is checked on the relation objects.
You only get objects that you are allowed to see.
Use the `unrestricted` parameter if you want to bypass this check.

To get back relations, so relations pointing to an item, use:

```python
friendships = api.relation.get(target=target)
```

% invisible-code-block: python
%
% self.assertEqual([friendship.from_object for friendship in friendships], [source])

To get the objects connected by relations you can use the api of these return values:

```python
for relation in api.relation.get(source=source):
    source = relation.from_object
    target = relation.to_object
    relationship = relation.from_attribute
```


(relation-create-example)=

## Create relation

To create a relation between source object and target object, use {meth}`api.relation.create`.

```python
from plone import api

portal = api.portal.get()
source = portal.bob
target = portal.bobby
api.relation.create(source=source, target=target, relationship="friend")
```

If the relation is based on a `RelationChoice` or `RelationList` field on the source object, the value of that field is created/updated accordingly.

(relation-delete-example)=

## Delete relation

Delete one or more relations:

```python
api.relation.delete(source=source, target=target, relationship="friend")
```

In order to delete relation(s), you must provide either `source`, `target`, or `relationship` to {meth}`api.relation.delete`.
You can mix and match.

Delete all relations from source to any target:

```python
api.relation.delete(source=source)
```

Delete all relations from any source to this target:

```python
api.relation.delete(target=target)
```

Delete relations with name "friend" from source to any target:

```python
api.relation.delete(source=source, relationship="friend")
```

Delete relations with name "uncle" from any source to this target:

```python
api.relation.delete(target=target, relationship="uncle")
```

Delete relations with name "enemy" from any source to any target:

```python
api.relation.delete(relationship="enemy")
```

If a deleted relation is based on a `RelationChoice` or `RelationList` field on the source object, the value of the field is removed/updated accordingly.

## Further reading

For more information on possible flags and usage options please see the full {ref}`plone-api-relation` specification.
For more information on relations read the relevant [chapter in the Mastering Plone training](https://training.plone.org/mastering-plone/relations.html).
