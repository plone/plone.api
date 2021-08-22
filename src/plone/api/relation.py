"""Module that provides functionality for relations.

Heavily inspired by collective.relationhelpers.
"""
from AccessControl.SecurityManagement import getSecurityManager
from collections import defaultdict
from plone.api.exc import InvalidParameterError
from plone.api.validation import at_least_one_of
from plone.api.validation import required_parameters
from plone.app.iterate.dexterity import ITERATE_RELATION_NAME
from plone.app.iterate.dexterity.relation import StagingRelationValue
from plone.app.linkintegrity.handlers import modifiedContent
from plone.app.linkintegrity.utils import referencedRelationship
from plone.dexterity.utils import iterSchemataForType
from Products.CMFPlone.utils import base_hasattr
from z3c.relationfield import event
from z3c.relationfield import RelationValue
from z3c.relationfield.schema import Relation
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import modified

import logging


logger = logging.getLogger(__name__)


def _get_field_and_schema_for_fieldname(field_id, portal_type):
    """Get field and its schema from a portal_type."""
    # Turn form.widgets.IDublinCore.title into title
    field_id = field_id.split('.')[-1]
    for schema in iterSchemataForType(portal_type):
        field = schema.get(field_id, None)
        if field is not None:
            return (field, schema)


@required_parameters('source', 'target', 'relationship')
def create(source=None, target=None, relationship=None):
    """Create a relation from source to target using zc.relation

    If source is dexterity content, and the relationship name is the same
    as a field name, and this field is a RelationChoice/RelationList/Relation,
    we will add the relation as attribute.

    Other relations will only be added to the relation-catalog.

    Adapted from collective.relationhelpers link_objects.
    """
    if source is not None and not base_hasattr(source, 'portal_type'):
        raise InvalidParameterError('{} has no portal_type'.format(source))

    if target is not None and not base_hasattr(target, 'portal_type'):
        raise InvalidParameterError('{} has no portal_type'.format(target))

    if not isinstance(relationship, str):
        raise InvalidParameterError('{} is no string'.format(relationship))

    relation_catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    to_id = intids.getId(target)
    from_id = intids.getId(source)
    from_attribute = relationship

    # Check if there is exactly this relation.
    # If so remove it and create a fresh one.
    query = {
        'from_attribute': from_attribute,
        'from_id': from_id,
        'to_id': to_id,
    }
    for rel in relation_catalog.findRelations(query):
        relation_catalog.unindex(rel)

    if from_attribute == referencedRelationship:
        # Don't mess with linkintegrity-relations!
        # Refresh them by triggering this subscriber.
        modifiedContent(source, None)
        return

    if (
        ITERATE_RELATION_NAME is not None
        and from_attribute == ITERATE_RELATION_NAME
    ):
        # Iterate relations use a subclass of RelationValue
        relation = StagingRelationValue(to_id)
        event._setRelation(source, ITERATE_RELATION_NAME, relation)
        return

    # This can only get a field from a dexterity item.
    field_and_schema = _get_field_and_schema_for_fieldname(
        from_attribute,
        source.portal_type,
    )

    if field_and_schema is None:
        # The relationship is not the name of a dexterity field.
        # Only create a relation.
        logger.debug(
            'No dexterity field. Setting relation %s from %s to %s',
            source.absolute_url(),
            target.absolute_url(),
            relationship,
        )
        event._setRelation(source, from_attribute, RelationValue(to_id))
        return

    field, _schema = field_and_schema

    if isinstance(field, RelationList):
        logger.info(
            'Add relation to relationlist %s from %s to %s',
            from_attribute,
            source.absolute_url(),
            target.absolute_url(),
        )
        existing_relations = getattr(source, from_attribute, [])
        existing_relations.append(RelationValue(to_id))
        setattr(source, from_attribute, existing_relations)
        modified(source)
        return

    elif isinstance(field, (Relation, RelationChoice)):
        logger.info(
            'Add relation %s from %s to %s',
            from_attribute,
            source.absolute_url(),
            target.absolute_url(),
        )
        setattr(source, from_attribute, RelationValue(to_id))
        modified(source)
        return

    # If we end up here, someone is making a relationship that
    # has the same name as a non-relation field.
    # This can be harmless coincidence, and this could be an error,
    # indicating that the field is of the wrong type.
    # Let's create the relationship and log a warning.
    event._setRelation(source, from_attribute, RelationValue(to_id))
    logger.warning(
        'Created relation %s on an item that has a field with the same name '
        'which is not a relation field. Is this what you wanted? '
        'Relation points from %s to %s',
        from_attribute,
        source.absolute_url(),
        target.absolute_url(),
    )


@at_least_one_of('source', 'target', 'relationship', 'delete_all')
def delete(source=None, target=None, relationship=None, delete_all=False):
    """Delete relation or relations.

    If you specify 'delete_all=True' and none of the other parameters,
    we delete all relations.

    TODO: do we want to remove RelationValues from content objects?
    """
    if source is not None and not base_hasattr(source, 'portal_type'):
        raise InvalidParameterError('{} has no portal_type'.format(source))

    if target is not None and not base_hasattr(target, 'portal_type'):
        raise InvalidParameterError('{} has no portal_type'.format(target))

    if relationship is not None and not isinstance(
        relationship,
        str,
    ):
        raise InvalidParameterError('{} is no string'.format(relationship))

    if delete_all and (source or target or relationship is not None):
        raise InvalidParameterError(
            'When you use delete_all, you must not use any other parameters.',
        )

    query = {}
    relation_catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    if source is not None:
        query['from_id'] = intids.getId(source)
    if target is not None:
        query['to_id'] = intids.getId(target)
    if relationship is not None:
        query['from_attribute'] = relationship
    if not query:
        relation_catalog.clear()
        return
    for rel in relation_catalog.findRelations(query):
        relation_catalog.unindex(rel)


@at_least_one_of('source', 'target', 'relationship')
def get(
    source=None,
    target=None,
    relationship=None,
    unrestricted=False,
    as_dict=False,
):
    """Get specific relations given a source/target/relationship

    Copied and modified from collective.relationhelpers get_relations.
    """
    if source is not None and not base_hasattr(source, 'portal_type'):
        raise InvalidParameterError('{} has no portal_type'.format(source))

    if target is not None and not base_hasattr(target, 'portal_type'):
        raise InvalidParameterError('{} has no portal_type'.format(target))

    if relationship is not None and not isinstance(
        relationship,
        str,
    ):
        raise InvalidParameterError('{} is no string'.format(relationship))

    intids = getUtility(IIntIds)
    relation_catalog = getUtility(ICatalog)
    query = {}
    results = []

    if as_dict:
        results = defaultdict(list)

    if not relation_catalog:
        return results

    if not unrestricted:
        checkPermission = getSecurityManager().checkPermission

    if source is not None:
        query['from_id'] = intids.getId(source)
    if target is not None:
        query['to_id'] = intids.getId(target)
    if relationship is not None:
        query['from_attribute'] = relationship

    for relation in relation_catalog.findRelations(query):
        if relation.isBroken():
            continue

        if not unrestricted:
            source_obj = relation.from_object
            target_obj = relation.to_object

            if checkPermission('View', source_obj) and checkPermission(
                'View',
                target_obj,
            ):
                if as_dict:
                    results[relation.from_attribute].append(relation)
                else:
                    results.append(relation)
            else:
                continue
        else:
            if as_dict:
                results[relation.from_attribute].append(relation)
            else:
                results.append(relation)
    return results
