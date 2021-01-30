# -*- coding: utf-8 -*-
"""Module that provides functionality for relations.

Heavily inspired by collective.relationhelpers.
"""
from AccessControl.SecurityManagement import getSecurityManager
from collections import Counter
from collections import defaultdict
from five.intid.intid import addIntIdSubscriber
from plone import api
from plone.app.iterate.dexterity import ITERATE_RELATION_NAME
from plone.app.iterate.dexterity.relation import StagingRelationValue
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


def create(source=None, target=None, relationship=""):
    """Create a relation from source to target using zc.relation

    For RelationChoice or RelationList it will add the relation as attribute.
    Other relations they will only be added to the relation-catalog.

    Copied from collective.relationhelpers link_objects.
    """
    if not IDexterityContent.providedBy(source):
        logger.info(u'{} is no dexterity content'.format(source.portal_type))
        return

    if not IDexterityContent.providedBy(target):
        logger.info(u'{} is no dexterity content'.format(target.portal_type))
        return

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

    if from_attribute == ITERATE_RELATION_NAME:
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


def delete(source=None, target=None, relationship=""):
    """Delete relation or relations."""
    pass


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


def get(obj, attribute=None, backrels=False, restricted=True, as_dict=False):
    """Get specific relations or backrelations for a content object

    Copied from collective.relationhelpers get_relations.
    We may want to have these keyword arguments instead:
    source=None, target=None, relationship=""
    """
    if not IDexterityContent.providedBy(obj):
        logger.info(u'{} is no dexterity content'.format(obj))
        return

    results = []
    if as_dict:
        results = defaultdict(list)
    int_id = _get_intid(obj)
    if not int_id:
        return results

    relation_catalog = getUtility(ICatalog)
    if not relation_catalog:
        return results

    query = {}
    if backrels:
        query['to_id'] = int_id
    else:
        query['from_id'] = int_id

    if restricted:
        checkPermission = getSecurityManager().checkPermission

    if attribute and isinstance(attribute, (list, tuple)):
        # The relation-catalog does not support queries for multiple from_attributes
        # We make multiple queries to support this use-case.
        relations = []
        for from_attribute in attribute:
            query['from_attribute'] = from_attribute
            relations.extend(relation_catalog.findRelations(query))
    elif attribute:
        # query with one attribute
        query['from_attribute'] = attribute
        relations = relation_catalog.findRelations(query)
    else:
        # query without constraint on a attribute
        relations = relation_catalog.findRelations(query)

    for relation in relations:
        if relation.isBroken():
            continue

        if backrels:
            obj = relation.from_object
        else:
            obj = relation.to_object

        if as_dict:
            if restricted:
                if checkPermission('View', obj):
                    results[relation.from_attribute].append(obj)
                else:
                    results[relation.from_attribute].append(None)
            else:
                results[relation.from_attribute].append(obj)
        else:
            if restricted:
                if checkPermission('View', obj):
                    results.append(obj)
            else:
                results.append(obj)
    return results
