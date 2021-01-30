# -*- coding: utf-8 -*-
"""Module that provides functionality for relations.

Heavily inspired by collective.relationhelpers.
"""
from AccessControl.SecurityManagement import getSecurityManager
from collections import Counter
from collections import defaultdict
from five.intid.intid import addIntIdSubscriber
from plone import api
from plone.api.exc import InvalidParameterError
from plone.api.validation import at_least_one_of
from plone.api.validation import mutually_exclusive_parameters
from plone.api.validation import required_parameters
from plone.app.linkintegrity.handlers import modifiedContent
from plone.app.linkintegrity.utils import referencedRelationship
from plone.app.relationfield.event import update_behavior_relations
from plone.app.uuid.utils import uuidToObject
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import iterSchemataForType
from Products.CMFCore.interfaces import IContentish
from Products.Five.browser import BrowserView
from z3c.relationfield import event
from z3c.relationfield import RelationValue
from z3c.relationfield.event import updateRelations
from z3c.relationfield.schema import Relation
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zc.relation.interfaces import ICatalog
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.component import queryUtility
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import modified

import json
import logging
import six

try:
    from plone.app.iterate.dexterity import ITERATE_RELATION_NAME
    from plone.app.iterate.dexterity.relation import StagingRelationValue
except ImportError:
    ITERATE_RELATION_NAME = None
    StagingRelationValue = None

logger = logging.getLogger(__name__)


def _get_field_and_schema_for_fieldname(field_id, fti):
    """Get field and its schema from a fti.
    """
    # Turn form.widgets.IDublinCore.title into title
    field_id = field_id.split('.')[-1]
    for schema in iterSchemataForType(fti):
        field = schema.get(field_id, None)
        if field is not None:
            return (field, schema)


@required_parameters('source', 'target', 'relationship')
def create(source=None, target=None, relationship=None):
    """Create a relation from source to target using zc.relation

    For RelationChoice or RelationList it will add the relation as attribute.
    Other relations they will only be added to the relation-catalog.

    Copied from collective.relationhelpers link_objects.
    """
    if not IDexterityContent.providedBy(source):
        raise InvalidParameterError('{} is no dexterity content'.format(source))

    if not IDexterityContent.providedBy(target):
        raise InvalidParameterError('{} is no dexterity content'.format(target))

    if not isinstance(relationship, six.string_types):
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

    if ITERATE_RELATION_NAME is not None and from_attribute == ITERATE_RELATION_NAME:
        # Iterate relations use a subclass of RelationValue
        relation = StagingRelationValue(to_id)
        event._setRelation(source, ITERATE_RELATION_NAME, relation)
        return

    fti = queryUtility(IDexterityFTI, name=source.portal_type)
    if not fti:
        logger.info(u'{} is no dexterity content'.format(source.portal_type))
        return
    field_and_schema = _get_field_and_schema_for_fieldname(from_attribute, fti)

    if field_and_schema is None:
        # The relationship is not the name of a field. Only create a relation.
        logger.info(u'No field. Setting relation {} from {} to {}'.format(
            source.absolute_url(), target.absolute_url(), relationship))
        event._setRelation(source, from_attribute, RelationValue(to_id))
        return

    field, schema = field_and_schema

    if isinstance(field, RelationList):
        logger.info('Add relation to relationlist {} from {} to {}'.format(
            from_attribute, source.absolute_url(), target.absolute_url()))
        existing_relations = getattr(source, from_attribute, [])
        existing_relations.append(RelationValue(to_id))
        setattr(source, from_attribute, existing_relations)
        modified(source)
        return

    elif isinstance(field, (Relation, RelationChoice)):
        logger.info('Add relation {} from {} to {}'.format(
            from_attribute, source.absolute_url(), target.absolute_url()))
        setattr(source, from_attribute, RelationValue(to_id))
        modified(source)
        return

    # We should never end up here!
    logger.info('Warning: Unexpected relation {} from {} to {}'.format(
        from_attribute, source.absolute_url(), target.absolute_url()))


# @at_least_one_of('source', 'target', 'relationship')
def delete(source=None, target=None, relationship=""):
    """Delete relation or relations.

    If you do not specify any parameters, we delete all relations.

    TODO: do we want to remove RelationValues from content objects?
    """
    if source is not None and not IDexterityContent.providedBy(source):
        raise InvalidParameterError('{} is no dexterity content'.format(source))

    if target is not None and not IDexterityContent.providedBy(target):
        raise InvalidParameterError('{} is no dexterity content'.format(target))

    if relationship is not None and not isinstance(relationship, six.string_types):
        raise InvalidParameterError('{} is no string'.format(relationship))

    query = {}
    relation_catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    if source is not None:
        query['from_id'] = intids.getId(source)
    if target is not None:
        query['to_id'] = intids.getId(target)
    if relationship is not None:
        query['from_attribute'] = relationship
    # If the query is empty, we could do relation_catalog.clear().
    for rel in relation_catalog.findRelations(query):
        relation_catalog.unindex(rel)


def _get_intid(obj):
    """Intid from intid-catalog"""
    intids = queryUtility(IIntIds)
    if intids is None:
        return
    # check that the object has an intid, otherwise there's nothing to be done
    try:
        return intids.getId(obj)
    except KeyError:  # noqa
        # The object has not been added to the ZODB yet
        return

def get(source=None, target=None, relationship="",
        unrestricted=False, as_dict=False):
    """Get specific relations or backrelations for a content object

    Copied from collective.relationhelpers get_relations.
    We may want to have these keyword arguments instead:
    source=None, target=None, relationship=""
    """
    # No longer needed since you can query by relationship alone
    # if not IDexterityContent.providedBy(obj):
    #     logger.info(u'{} is no dexterity content'.format(obj))
    #     return

    intids = getUtility(IIntIds)
    to_id = intids.getId(target)
    from_id = intids.getId(source)
    from_attribute = relationship
    relation_catalog = getUtility(ICatalog)
    results = []

    if as_dict:
        results = defaultdict(list)

    if not relation_catalog:
        return results

    if not unrestricted:
        checkPermission = getSecurityManager().checkPermission

    query = {
        'from_attribute': from_attribute,
        'from_id': from_id,
        'to_id': to_id,
    }

    for relation in relation_catalog.findRelations(query):
        if relation.isBroken():
            continue

        if not unrestricted:
            source_obj = relation.from_object
            target_obj = relation.to_object

            if checkPermission('View', source_obj) and checkPermission('View', target_obj):
                if as_dict:
                    results[relation.__hash__].append(relation)
                else:
                    results.append(relation)
            else:
                continue
        else:
            if as_dict:
                results[relation.__hash__].append(relation)
            else:
                results.append(relation)
    return results
