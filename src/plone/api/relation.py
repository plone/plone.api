"""Module that provides functionality for relations.

Heavily inspired by collective.relationhelpers.
"""

from AccessControl.SecurityManagement import getSecurityManager
from collections import defaultdict
from importlib.metadata import distribution
from importlib.metadata import PackageNotFoundError
from plone.api.exc import InvalidParameterError
from plone.api.validation import at_least_one_of
from plone.api.validation import required_parameters
from plone.app.linkintegrity.handlers import modifiedContent
from plone.app.linkintegrity.utils import referencedRelationship
from plone.base.utils import base_hasattr
from plone.dexterity.utils import iterSchemataForType
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


try:
    distribution("plone.app.iterate")
except PackageNotFoundError:
    ITERATE_RELATION_NAME = None
    StagingRelationValue = None
else:
    from plone.app.iterate.dexterity import ITERATE_RELATION_NAME
    from plone.app.iterate.dexterity.relation import StagingRelationValue


logger = logging.getLogger(__name__)


def _get_field_and_schema_for_fieldname(field_id, portal_type):
    """Get field and its schema from a portal_type."""
    # Turn form.widgets.IDublinCore.title into title
    field_id = field_id.split(".")[-1]
    for schema in iterSchemataForType(portal_type):
        field = schema.get(field_id, None)
        if field is not None:
            return (field, schema)


@at_least_one_of("source", "target", "relationship")
def get(
    source=None,
    target=None,
    relationship=None,
    unrestricted=False,
    as_dict=False,
):
    """Get specific relations given a source/target/relationship.

    :param source: Object that the relations originate from.
    :type source: Content object
    :param target: Object that the relations point to.
    :type target: Content object
    :param relationship: Relationship name.
    :type id: string
    :param unrestricted: If true bypass permission-check on source and target.
    :type id: boolean
    :param as_dict: If true, return a dictionary with the relationship
        name as keys.
    :type id: bool
    :returns: A list of relations
    :rtype: List of RelationValue objects

    :Example: :ref:`relation-get-example`
    """
    if source is not None and not base_hasattr(source, "portal_type"):
        raise InvalidParameterError(f"{source} has no portal_type")

    if target is not None and not base_hasattr(target, "portal_type"):
        raise InvalidParameterError(f"{target} has no portal_type")

    if relationship is not None and not isinstance(
        relationship,
        str,
    ):
        raise InvalidParameterError(f"{relationship} is no string")

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
        query["from_id"] = intids.getId(source)
    if target is not None:
        query["to_id"] = intids.getId(target)
    if relationship is not None:
        query["from_attribute"] = relationship

    for relation in relation_catalog.findRelations(query):
        if relation.isBroken():
            continue

        if not unrestricted:
            source_obj = relation.from_object
            target_obj = relation.to_object

            if checkPermission("View", source_obj) and checkPermission(
                "View",
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


@required_parameters("source", "target", "relationship")
def create(source=None, target=None, relationship=None):
    """Create a relation from source to target using zc.relation.

    :param source: [required] Object that the relation will originate from.
    :type source: Content object
    :param target: [required] Object that the relation will point to.
    :type target: Content object
    :param relationship: [required] Relationship name.
        If that name is the same as a field name and this field
        is a RelationChoice / RelationList
        we will update the field-value accordingly.
    :type id: string
    :Example: :ref:`relation-create-example`
    """
    if source is not None and not base_hasattr(source, "portal_type"):
        raise InvalidParameterError(f"{source} has no portal_type")

    if target is not None and not base_hasattr(target, "portal_type"):
        raise InvalidParameterError(f"{target} has no portal_type")

    if not isinstance(relationship, str):
        raise InvalidParameterError(f"{relationship} is no string")

    relation_catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    to_id = intids.getId(target)
    from_id = intids.getId(source)
    from_attribute = relationship

    # Check if there is exactly this relation.
    # If so remove it and create a fresh one.
    query = {
        "from_attribute": from_attribute,
        "from_id": from_id,
        "to_id": to_id,
    }
    has_relation = (
        False
        if (len([el for el in relation_catalog.findRelations(query)]) == 0)
        else True
    )

    if from_attribute == referencedRelationship:
        # Don't mess with linkintegrity-relations!
        # Refresh them by triggering this subscriber.
        modifiedContent(source, None)
        return

    if ITERATE_RELATION_NAME is not None and from_attribute == ITERATE_RELATION_NAME:
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
            "No dexterity field. Setting relation %s from %s to %s",
            source.absolute_url(),
            target.absolute_url(),
            relationship,
        )
        event._setRelation(source, from_attribute, RelationValue(to_id))
        return

    field, _schema = field_and_schema

    if isinstance(field, RelationList):
        logger.info(
            "Add relation to relationlist %s from %s to %s",
            from_attribute,
            source.absolute_url(),
            target.absolute_url(),
        )
        if not has_relation:
            existing_relations = getattr(source, from_attribute, None) or []
            existing_relations.append(RelationValue(to_id))
            setattr(source, from_attribute, existing_relations)
            modified(source)
        return

    elif isinstance(field, (Relation, RelationChoice)):
        logger.info(
            "Add relation %s from %s to %s",
            from_attribute,
            source.absolute_url(),
            target.absolute_url(),
        )
        if not has_relation:
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
        "Created relation %s on an item that has a field with the same name "
        "which is not a relation field. Is this what you wanted? "
        "Relation points from %s to %s",
        from_attribute,
        source.absolute_url(),
        target.absolute_url(),
    )


@at_least_one_of("source", "target", "relationship")
def delete(source=None, target=None, relationship=None):
    """Delete relation or relations.

    :param source: Object that the relation originates from.
    :type source: Content object
    :param target: Object that the relation points to.
    :type target: Content object
    :param relationship: Relationship name.
        If that name is the same as a field name
        and this field is a RelationChoice/RelationList
        we will delete/update the field-value accordingly.
    :type id: string
    :Example: :ref:`relation-delete-example`
    """
    if source is not None and not base_hasattr(source, "portal_type"):
        raise InvalidParameterError(f"{source} has no portal_type")

    if target is not None and not base_hasattr(target, "portal_type"):
        raise InvalidParameterError(f"{target} has no portal_type")

    if relationship is not None and not isinstance(
        relationship,
        str,
    ):
        raise InvalidParameterError(f"{relationship} is no string")

    query = {}
    relation_catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    if source is not None:
        query["from_id"] = intids.getId(source)
    if target is not None:
        query["to_id"] = intids.getId(target)
    if relationship is not None:
        query["from_attribute"] = relationship
    # We'll change the bucket in the loop
    for rel in [rel for rel in relation_catalog.findRelations(query)]:
        source = rel.from_object
        from_attribute = rel.from_attribute
        field_and_schema = _get_field_and_schema_for_fieldname(
            from_attribute,
            source.portal_type,
        )
        if field_and_schema is None:
            # The relationship is not the name of a dexterity field.
            # Only purge relation from relation-catalog.
            relation_catalog.unindex(rel)
            continue

        target = rel.to_object
        field, _schema = field_and_schema
        if isinstance(field, RelationList):
            logger.info(
                "Remove relation from %s to %s from relationlist %s",
                source.absolute_url(),
                target.absolute_url(),
                from_attribute,
            )
            existing = getattr(source, from_attribute, [])
            updated_relations = [i for i in existing if i.to_object != target]
            setattr(source, from_attribute, updated_relations)
            modified(source)

        elif isinstance(field, (Relation, RelationChoice)):
            logger.info(
                "Remove relation %s from %s to %s",
                from_attribute,
                source.absolute_url(),
                target.absolute_url(),
            )
            delattr(source, from_attribute)
            modified(source)
        # unindex in case something went wrong with the automatic unindex
        relation_catalog.unindex(rel)
