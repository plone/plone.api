# -*- coding: utf-8 -*-
"""Tests for plone.api.content."""

from Acquisition import aq_base
from OFS.CopySupport import CopyError
from OFS.event import ObjectWillBeMovedEvent
from OFS.interfaces import IObjectWillBeMovedEvent
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.interfaces import IContentish
from Products.ZCatalog.interfaces import IZCatalog
from plone import api
from plone.api.content import NEW_LINKINTEGRITY
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.linkintegrity.exceptions import \
    LinkIntegrityNotificationException
from plone.app.textfield import RichTextValue
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from plone.uuid.interfaces import IMutableUUID
from plone.uuid.interfaces import IUUIDGenerator
from zExceptions import BadRequest
from zope.component import getGlobalSiteManager
from zope.component import getUtility
from zope.container.contained import ContainerModifiedEvent
from zope.lifecycleevent import IObjectModifiedEvent
from zope.lifecycleevent import IObjectMovedEvent
from zope.lifecycleevent import ObjectMovedEvent
from zope.lifecycleevent import modified

import mock
import pkg_resources
import unittest

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_PACONTENTYPES = False
else:
    HAS_PACONTENTYPES = True


class TestPloneApiContent(unittest.TestCase):
    """Unit tests for content manipulation using plone.api"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Create a portal structure which we can test against.

        Plone (portal root)
        |-- image
        |-- blog
        |-- about
        |   |-- team
        |   `-- contact
        `-- events
            |-- training
            |-- conference
            `-- sprint
        """
        self.portal = self.layer['portal']

        self.blog = api.content.create(
            type='Link', id='blog', container=self.portal)
        self.about = api.content.create(
            type='Folder', id='about', container=self.portal)
        self.events = api.content.create(
            type='Folder', id='events', container=self.portal)

        self.team = api.content.create(
            container=self.about, type='Document', id='team')
        self.contact = api.content.create(
            container=self.about, type='Document', id='contact')

        self.training = api.content.create(
            container=self.events, type='Event', id='training')
        self.conference = api.content.create(
            container=self.events, type='Event', id='conference')
        self.sprint = api.content.create(
            container=self.events, type='Event', id='sprint')

        self.image = api.content.create(
            container=self.portal, type='Image', id='image')

    def test_create_constraints(self):
        """Test the constraints when creating content."""
        from plone.api.exc import InvalidParameterError
        from plone.api.exc import MissingParameterError

        # This will definitely fail
        with self.assertRaises(MissingParameterError):
            api.content.create()

        # Check the contraints for the type container
        with self.assertRaises(MissingParameterError):
            api.content.create(
                type='Document',
                id='test-doc',
            )

        # Check the contraints for the type parameter
        container = mock.Mock()
        with self.assertRaises(MissingParameterError):
            api.content.create(
                container=container,
                id='test-doc',
            )

        # Check the contraints for id and title parameters
        with self.assertRaises(MissingParameterError):
            api.content.create(
                container=container, type='Document'
            )

        # Check the contraints for allowed types in the container
        container = self.events
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=container,
                type='foo',
                id='test-foo',
            )

        # Check the contraints for allowed types in the container if
        # the container is the portal
        container = self.portal
        with self.assertRaises(InvalidParameterError) as cm:
            api.content.create(
                container=container,
                type='foo',
                id='test-foo'
            )

        # Check if the underlying error message is included
        # in the InvalidParameterError message
        self.assertIn(
            "No such content type: foo",
            cm.exception.message
        )

        # Check the contraints for allowed types in the container
        # Create a folder
        folder = api.content.create(
            container=container, type='Folder', id='test-folder')
        assert folder

        # Constraint the allowed types
        ENABLED = 1
        if getattr(aq_base(folder), 'setConstrainTypesMode', None):  # AT
            folder.setConstrainTypesMode(ENABLED)
            folder.setLocallyAllowedTypes(('News Item',))
        else:  # DX
            from Products.CMFPlone.interfaces import ISelectableConstrainTypes
            constraints = ISelectableConstrainTypes(folder)
            constraints.setConstrainTypesMode(ENABLED)
            constraints.setLocallyAllowedTypes(('News Item',))

        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=folder,
                type='Document',
                id='test-doc'
            )

    def test_create_dexterity(self):
        """Test create dexterity"""
        container = self.portal

        # This section check for DX compatibilty. The custom DX types defined
        # in plone.api are for Plone 4 compatiblity.

        # Create a folder
        folder = api.content.create(
            container=container, type='Dexterity Folder', id='test-folder')
        assert folder
        self.assertEqual(folder.id, 'test-folder')
        self.assertEqual(folder.portal_type, 'Dexterity Folder')

        # Create an item
        page = api.content.create(
            container=folder, type='Dexterity Item', id='test-item')
        assert page
        self.assertEqual(page.id, 'test-item')
        self.assertEqual(page.portal_type, 'Dexterity Item')

        # Create an item with a title and without an id
        page = api.content.create(
            container=folder,
            type='Dexterity Item',
            title='Test id generated'
        )
        assert page
        self.assertEqual(page.id, 'test-id-generated')
        self.assertEqual(page.Title(), 'Test id generated')
        self.assertEqual(page.portal_type, 'Dexterity Item')

        # Try to create another item with same id, this should fail
        with self.assertRaises(BadRequest):
            api.content.create(
                container=folder,
                type='Dexterity Item',
                id='test-item',
            )

    def test_create_content(self):
        """Test create content"""
        container = self.portal

        # This section below is either AT (Plone < 5) or DX (Plone >= 5)
        # We use Products.ATContentTypes in Plone 4 or plone.app.contenttypes
        # in Plone 5

        # Create a folder
        folder = api.content.create(
            container=container, type='Folder', id='test-folder')
        assert folder
        self.assertEqual(folder.id, 'test-folder')
        self.assertEqual(folder.portal_type, 'Folder')

        # Create a document
        page = api.content.create(
            container=folder, type='Document', id='test-document')
        assert page
        self.assertEqual(page.id, 'test-document')
        self.assertEqual(page.portal_type, 'Document')

        # Create a document with a title and without an id
        page = api.content.create(
            container=folder, type='Document', title='Test id generated')
        assert page
        self.assertEqual(page.id, 'test-id-generated')
        self.assertEqual(page.Title(), 'Test id generated')
        self.assertEqual(page.portal_type, 'Document')

        # Try to create another page with same id, this should fail
        with self.assertRaises(BadRequest):
            api.content.create(
                container=folder,
                type='Document',
                id='test-document',
            )

    def test_create_with_safe_id(self):
        """Test the content creating with safe_id mode."""
        container = self.portal

        first_page = api.content.create(
            container=container,
            type='Document',
            id='test-document',
            safe_id=True,
        )
        assert first_page
        self.assertEqual(first_page.id, 'test-document')
        self.assertEqual(first_page.portal_type, 'Document')

        # Second page is created with non-conflicting id
        second_page = api.content.create(
            container=container,
            type='Document',
            id='test-document',
            safe_id=True,
        )
        assert second_page
        self.assertEqual(second_page.id, 'test-document-1')
        self.assertEqual(second_page.portal_type, 'Document')

    def test_create_raises_unicodedecodeerror(self):
        """Test that the create method raises UnicodeDecodeErrors correctly."""
        site = getGlobalSiteManager()
        unicode_exception_message = "This is a fake unicode error"

        # register a title indexer that will force a UnicodeDecodeError
        # during content reindexing
        @indexer(IContentish, IZCatalog)
        def force_unicode_error(object):
            raise UnicodeDecodeError('ascii', 'x', 1, 5,
                                     unicode_exception_message)

        site.registerAdapter(factory=force_unicode_error, name='Title')

        def unregister_indexer():
            site.unregisterAdapter(factory=force_unicode_error, name='Title')

        self.addCleanup(unregister_indexer)

        with self.assertRaises(UnicodeDecodeError) as ude:
            api.content.create(
                type='Folder', id='test-unicode-folder',
                container=self.portal,
            )

        # check that the exception is the one we raised
        self.assertEqual(ude.exception.reason, unicode_exception_message)

    def test_get_constraints(self):
        """Test the constraints when content is fetched with get."""

        # Path and UID parameter can not be given together
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.content.get(
                path='/',
                UID='dummy'
            )

        # Either a path or UID must be given
        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.content.get()

    def test_get(self):
        """Test the getting of content in varios ways."""

        # Test getting the about folder by path and UID
        about_by_path = api.content.get('/about')
        about_by_uid = api.content.get(UID=self.about.UID())
        self.assertEqual(self.about, about_by_path)
        self.assertEqual(self.about, about_by_uid)

        # Test getting the team document by path and UID
        team_by_path = api.content.get('/about/team')
        team_by_uid = api.content.get(UID=self.team.UID())
        self.assertEqual(self.team, team_by_path)
        self.assertEqual(self.team, team_by_uid)

        # Test getting the team document by path that has portal id included
        team_by_path = api.content.get(
            '/{0}/about/team'.format(self.portal.getId()))
        self.assertEqual(self.team, team_by_path)

        # Test getting an non-existing item by path and UID
        self.assertFalse(api.content.get('/spam/ham'))
        self.assertFalse(api.content.get(UID='bacon'))

        # Test getting a non-existing subfolder by path
        self.assertFalse(api.content.get('/about/spam'))

    def test_move_constraints(self):
        """Test the constraints for moving content."""
        from plone.api.exc import MissingParameterError

        # When no parameters are given an error is raised
        with self.assertRaises(MissingParameterError):
            api.content.move()

        container = mock.Mock()

        # Source is missing an should raise an error
        with self.assertRaises(MissingParameterError):
            api.content.move(source=container)

        # Target is missing an should raise an error
        with self.assertRaises(MissingParameterError):
            api.content.move(target=container)

    def test_move(self):
        """Test moving of content."""

        container = self.portal

        # Move contact to the same folder (basically a rename)
        nucontact = api.content.move(source=self.contact, id='nu-contact')
        assert (container['about']['nu-contact'] and
                container['about']['nu-contact'] == nucontact)
        assert 'contact' not in container['about'].keys()

        # Move team page to portal root
        team = api.content.move(source=self.team, target=container)
        assert container['team'] and container['team'] == team
        assert 'team' not in container['about'].keys()

        # When moving objects we can change the id
        team = container['team']
        ourteam = api.content.move(source=team,
                                   target=self.about,
                                   id='our-team')
        assert (container['about']['our-team'] and
                container['about']['our-team'] == ourteam)
        assert 'team' not in container.keys()

        # Test with safe_id option when moving content
        api.content.create(
            container=self.about, type='Link', id='link-to-blog')
        linktoblog1 = api.content.move(
            source=self.blog,
            target=self.about,
            id='link-to-blog',
            safe_id=True,
        )
        assert (container['about']['link-to-blog-1'] and
                container['about']['link-to-blog-1'] == linktoblog1)
        assert 'link-to-blog' not in container.keys()

        api.content.move(source=self.conference, id='conference-renamed')
        self.assertEqual(self.conference.id, 'conference-renamed')

        # Move folderish object
        about = api.content.move(source=container.about,
                                 target=container.events)
        assert (container['events']['about'] and
                container['events']['about'] == about)

    def test_rename_constraints(self):
        """Test the constraints for rename content."""
        from plone.api.exc import MissingParameterError

        # When no parameters are given an error is raised
        with self.assertRaises(MissingParameterError):
            api.content.rename()

        container = mock.Mock()
        # Source is missing an should raise an error
        with self.assertRaises(MissingParameterError):
            api.content.rename(obj=container)

    def test_rename(self):
        """Test renaming of content."""

        container = self.portal
        sm = getGlobalSiteManager()
        firedEvents = []

        def recordEvent(event):
            firedEvents.append(event.__class__)

        sm.registerHandler(recordEvent, (IObjectWillBeMovedEvent,))
        sm.registerHandler(recordEvent, (IObjectMovedEvent,))
        sm.registerHandler(recordEvent, (IObjectModifiedEvent,))

        # Rename contact
        nucontact = api.content.rename(obj=self.contact, new_id='nu-contact')
        assert (container['about']['nu-contact'] and
                container['about']['nu-contact'] == nucontact)
        assert 'contact' not in container['about'].keys()

        self.assertItemsEqual(firedEvents, [
            ObjectMovedEvent,
            ObjectWillBeMovedEvent,
            ContainerModifiedEvent
        ])
        sm.unregisterHandler(recordEvent, (IObjectWillBeMovedEvent,))
        sm.unregisterHandler(recordEvent, (IObjectMovedEvent,))
        sm.unregisterHandler(recordEvent, (IObjectModifiedEvent,))

        # Test with safe_id option when moving content
        api.content.create(
            container=self.about, type='Link', id='link-to-blog')
        linktoblog1 = api.content.rename(
            obj=container['about']['link-to-blog'],
            new_id='link-to-blog',
            safe_id=True,
        )
        assert (container['about']['link-to-blog-1'] and
                container['about']['link-to-blog-1'] == linktoblog1)
        assert 'link-to-blog' not in container.keys()

        # Rename to existing id
        api.content.create(
            container=self.about, type='Link', id='link-to-blog')

        with self.assertRaises(CopyError):
            api.content.rename(
                obj=container['about']['link-to-blog'],
                new_id='link-to-blog-1',
            )
        linktoblog11 = api.content.rename(
            obj=container['about']['link-to-blog'],
            new_id='link-to-blog-1',
            safe_id=True,
        )
        assert (container['about']['link-to-blog-1-1'] and
                container['about']['link-to-blog-1-1'] == linktoblog11)
        assert 'link-to-blog' not in container.keys()

    def test_rename_same_folder(self):
        # When renaming a folderish item with safe_id=True, and there is
        # already an existing folderish item with that id, it should choose
        # a new name.

        events = self.portal['events']
        about = self.portal['about']
        api.content.rename(
            obj=events,
            new_id='about',
            safe_id=True
        )

        assert self.portal['about']
        assert self.portal['about-1']
        assert self.portal['about'].aq_base is about.aq_base
        assert self.portal['about-1'].aq_base is events.aq_base

    def test_copy_constraints(self):
        """Test the constraints for moving content."""
        from plone.api.exc import MissingParameterError

        # When no parameters are given an error is raised
        with self.assertRaises(MissingParameterError):
            api.content.copy()

        container = mock.Mock()
        # Source is missing and should raise an error
        with self.assertRaises(MissingParameterError):
            api.content.copy(source=container)

    def test_copy(self):
        """Test the copying of content."""

        container = self.portal

        # Copy team page to portal root
        team = api.content.copy(source=self.team, target=container)
        assert container['team'] and container['team'] == team
        assert (
            container['about']['team'] and
            container['about']['team'] != team
        )  # old content still available

        # When copying objects we can change the id
        ourteam = api.content.copy(source=self.team,
                                   target=self.about,
                                   id='our-team')
        assert (container['about']['our-team'] and
                container['about']['our-team'] == ourteam)

        # When copying whithout target parameter should take source parent
        api.content.copy(source=self.team, id='our-team-no-target')
        assert container['about']['our-team-no-target']

        # Test the safe_id option when moving content
        api.content.create(
            container=self.about, type='Link', id='link-to-blog')

        linktoblog1 = api.content.copy(
            source=self.blog,
            target=self.about,
            id='link-to-blog',
            safe_id=True,
        )
        assert (container['about']['link-to-blog-1'] and
                container['about']['link-to-blog-1'] == linktoblog1)

        # Copy folderish content under target
        about = api.content.copy(source=container.about,
                                 target=container.events)
        assert (container['events']['about'] and
                container['events']['about'] == about)

        # When copying with safe_id=True, the prior created item should not be
        # renamed, and the copied item should have a sane postfix

        # Create a products folder
        products = api.content.create(
            type='Folder', id='products', container=self.portal)

        # Create a item inside the products folder
        item = api.content.create(
            container=products, type='Document', id='item')

        api.content.copy(source=item, id='item', safe_id=True)

        assert container['products']['item-1']
        assert container['products']['item']

        # When copying with safe_id=True, the created bargain with the id=item
        # should not be renamed, and the item copied from the products folder
        # should have a sane postfix.
        # The item in the the products folder should still exist.

        # Create a second folder named bargains
        bargains = api.content.create(
            type='Folder', id='bargains', container=self.portal)

        # Create a bargain inside the bargains folder with the id="item"
        bargain = api.content.create(
            container=bargains, type='Document', id='item')
        api.content.copy(source=item, target=bargains, id='item', safe_id=True)

        assert container['bargains']['item-1']
        assert container['bargains']['item']
        assert container['bargains']['item'].aq_base is bargain.aq_base
        assert container['products']['item']

    def test_delete_constraints(self):
        """Test the constraints for deleting content."""

        # When no parameters are given an error is raised
        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.content.delete()

    def test_delete(self):
        """Test deleting a content item."""

        container = self.portal

        # The content item must be given as parameter
        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.content.delete()

        # Delete the contact page
        api.content.delete(self.contact)
        self.assertNotIn('contact', container['about'].keys())

    def test_delete_multiple(self):
        """Test deleting multiple content items."""

        container = self.portal
        api.content.copy(source=container['about'], target=container)
        api.content.copy(source=container['about'], target=container['events'])

        api.content.delete(objects=[container['copy_of_about'],
                                    container['events']['about']])
        self.assertNotIn('copy_of_about', container)
        self.assertNotIn('about', container['events'])

    def test_delete_ignore_linkintegrity(self):
        """Test deleting a content item with a link pointed at it."""
        self._set_text(self.team, '<a href="contact">contact</a>')
        # Delete the contact page
        api.content.delete(self.contact, check_linkintegrity=False)
        self.assertNotIn('contact', self.portal['about'].keys())

    @unittest.skipIf(
        HAS_PACONTENTYPES and not NEW_LINKINTEGRITY,
        'This test only makes sense with Archetypes or new Linkintegrity.')
    def test_delete_check_linkintegrity(self):
        """Test deleting a content item with a link pointed at it."""
        self._set_text(self.team, '<a href="contact">contact</a>')
        # Delete the contact page
        with self.assertRaises(LinkIntegrityNotificationException):
            api.content.delete(self.contact)
        if NEW_LINKINTEGRITY:
            # In the old implementation of linkintegrity the items are
            # still gone during this request.
            self.assertIn('contact', self.portal['about'].keys())

    @unittest.skipIf(
        HAS_PACONTENTYPES and not NEW_LINKINTEGRITY,
        'This test only makes sense with Archetypes or new Linkintegrity.')
    def test_delete_multiple_check_linkintegrity(self):
        """Test deleting multiple item with linkintegrity-breaches."""
        self._set_text(self.team, '<a href="../about/contact">contact</a>')
        self._set_text(self.training, '<a href="../blog">contact</a>')
        # Delete the contact page
        with self.assertRaises(LinkIntegrityNotificationException):
            api.content.delete(objects=[self.blog, self.contact])
        if NEW_LINKINTEGRITY:
            # In the old implementation of linkintegrity the items are
            # still gone during this request.
            self.assertIn('contact', self.portal['about'].keys())
            self.assertIn('blog', self.portal.keys())

    @unittest.skipIf(
        HAS_PACONTENTYPES and not NEW_LINKINTEGRITY,
        'This test only makes sense with Archetypes or new Linkintegrity.')
    def test_delete_multiple_ignore_linkintegrity(self):
        """Test deleting multiple items ignoring linkintegrity-breaches."""
        self._set_text(self.team, '<a href="../about/contact">contact</a>')
        self._set_text(self.training, '<a href="../blog">contact</a>')
        # Delete linked pages
        api.content.delete(
            objects=[self.blog, self.contact],
            check_linkintegrity=False)
        self.assertNotIn('contact', self.portal['about'].keys())
        self.assertNotIn('blog', self.portal.keys())

    @unittest.skipIf(
        HAS_PACONTENTYPES and not NEW_LINKINTEGRITY,
        'This test only makes sense with Archetypes or new Linkintegrity.')
    def test_delete_with_internal_breaches(self):
        """Test deleting multiple with internal linkintegrity breaches."""
        self._set_text(self.team, '<a href="../about/contact">contact</a>')
        self._set_text(self.training, '<a href="../blog">contact</a>')
        # Deleting pages with unresolved breaches throws an exception
        with self.assertRaises(LinkIntegrityNotificationException):
            api.content.delete(objects=[self.blog, self.about])
        if NEW_LINKINTEGRITY:
            # In the old implementation of linkintegrity the items are
            # still gone during this request.
            self.assertIn('about', self.portal.keys())
            self.assertIn('blog', self.portal.keys())
            self.assertIn('training', self.portal['events'].keys())

    @unittest.skipUnless(
        NEW_LINKINTEGRITY, 'Only new Linkintegrity resolves internal breaches')
    def test_delete_with_resolved_internal_breaches(self):
        """Test deleting multiple with internal linkintegrity breaches."""
        self._set_text(self.team, '<a href="../about/contact">contact</a>')
        self._set_text(self.training, '<a href="../blog">contact</a>')
        # Deleting pages with resolved breaches throws no exception
        api.content.delete(objects=[self.blog, self.training, self.about])
        self.assertNotIn('about', self.portal.keys())
        self.assertNotIn('blog', self.portal.keys())
        self.assertNotIn('training', self.portal['events'].keys())

    def _set_text(self, obj, text):
        if IDexterityContent.providedBy(obj):
            # Dexterity
            obj.text = RichTextValue(text)
        else:
            # Archetypes
            obj.setText(text, mimetype='text/html')
        modified(obj)

    def test_find(self):
        """Test the finding of content in various ways."""

        # Find documents
        documents = api.content.find(portal_type='Document')
        self.assertEqual(len(documents), 2)

    def test_find_empty_query(self):
        """Make sure an empty query yields no results"""

        documents = api.content.find()
        self.assertEqual(len(documents), 0)

    def test_find_invalid_indexes(self):
        """Make sure invalid indexes yield no results"""

        # All invalid indexes yields no results
        documents = api.content.find(invalid_index='henk')
        self.assertEqual(len(documents), 0)

        # But at least one valid index does.
        documents = api.content.find(
            invalid_index='henk', portal_type='Document')
        self.assertEqual(len(documents), 2)

    def test_find_context(self):
        # Find documents in context
        documents = api.content.find(
            context=self.portal.about, portal_type='Document')
        self.assertEqual(len(documents), 2)
        documents = api.content.find(
            context=self.portal.events, portal_type='Document')
        self.assertEqual(len(documents), 0)

    def test_find_depth(self):
        # Limit search depth from portal root
        documents = api.content.find(depth=2, portal_type='Document')
        self.assertEqual(len(documents), 2)
        documents = api.content.find(depth=1, portal_type='Document')
        self.assertEqual(len(documents), 0)

        # Limit search depth with explicit context
        documents = api.content.find(
            context=self.portal.about, depth=1, portal_type='Document')
        self.assertEqual(len(documents), 2)
        documents = api.content.find(
            context=self.portal.about, depth=0, portal_type='Document')
        self.assertEqual(len(documents), 0)

        # Limit search depth with explicit path
        documents = api.content.find(
            path='/'.join(self.portal.about.getPhysicalPath()),
            depth=1, portal_type='Document')
        self.assertEqual(len(documents), 2)
        documents = api.content.find(
            path='/'.join(self.portal.about.getPhysicalPath()),
            depth=0, portal_type='Document')
        self.assertEqual(len(documents), 0)
        documents = api.content.find(
            path='/'.join(self.portal.events.getPhysicalPath()),
            depth=1, portal_type='Document')
        self.assertEqual(len(documents), 0)

    def test_find_interface(self):
        # Find documents by interface or it's identifier
        identifier = IContentish.__identifier__
        brains = api.content.find(object_provides=identifier)
        by_identifier = [x.getObject() for x in brains]

        brains = api.content.find(object_provides=IContentish)
        by_interface = [x.getObject() for x in brains]

        self.assertEqual(by_identifier, by_interface)

    def test_find_dict(self):
        # Pass arguments using dict
        path = '/'.join(self.portal.about.getPhysicalPath())

        query = {
            'portal_type': 'Document',
            'path': {'query': path, 'depth': 2}
            }
        documents = api.content.find(**query)
        self.assertEqual(len(documents), 2)

        query = {
            'portal_type': 'Document',
            'path': {'query': path, 'depth': 0}
            }
        documents = api.content.find(**query)
        self.assertEqual(len(documents), 0)

        # This is a bit awkward, but it is nice if this does not crash.
        query = {
            'depth': 2,
            'portal_type': 'Document',
            'path': {'query': path}
            }
        documents = api.content.find(**query)
        self.assertEqual(len(documents), 2)

        path = '/'.join(self.portal.events.getPhysicalPath())
        query = {
            'depth': 2,
            'portal_type': 'Document',
            'path': {'query': path}
            }
        documents = api.content.find(**query)
        self.assertEqual(len(documents), 0)

    def test_get_state(self):
        """Test retrieving the workflow state of a content item."""

        # This should fail because an content item is mandatory
        from plone.api.exc import MissingParameterError
        with self.assertRaises(MissingParameterError):
            api.content.get_state()

        review_state = api.content.get_state(obj=self.blog)
        self.assertEqual(review_state, 'private')

    def test_get_state_default_value(self):
        """Test passing in a default value.
        """
        # A WorkflowException is raise if no workflow is defined for the obj.
        # This is normally the case for Images and Files.
        with self.assertRaises(WorkflowException):
            review_state = api.content.get_state(obj=self.image)

        default = 'my default value'
        review_state = api.content.get_state(obj=self.image, default=default)
        review_state is default

        # the default should not override the actual state.
        review_state = api.content.get_state(obj=self.blog, default=default)
        review_state is not default

    def test_transition(self):
        """Test transitioning the workflow state on a content item."""
        from plone.api.exc import InvalidParameterError
        from plone.api.exc import MissingParameterError

        with self.assertRaises(MissingParameterError):
            api.content.transition()

        with self.assertRaises(MissingParameterError):
            api.content.transition(obj=mock.Mock())

        with self.assertRaises(MissingParameterError):
            api.content.transition(transition='publish')

        with self.assertRaises(InvalidParameterError):
            api.content.transition(
                obj=mock.Mock(),
                transition='publish',
                to_state='published',
            )

        api.content.transition(obj=self.blog, transition='publish')
        review_state = api.content.get_state(obj=self.blog)
        self.assertEqual(review_state, 'published')

        # This should fail because the transition doesn't exist
        with self.assertRaises(InvalidParameterError) as cm:
            api.content.transition(
                transition='foo', obj=self.blog)

        self.maxDiff = None  # to see assert diff
        self.assertMultiLineEqual(
            str(cm.exception),
            "Invalid transition 'foo'.\n"
            "Valid transitions are:\n"
            "reject\n"
            "retract"
        )

        # change the workflow of a document so that there is no transition
        # that goes directly from one state to another
        portal_workflow = api.portal.get_tool('portal_workflow')
        portal_workflow._chains_by_type['File'] = tuple(
            ['intranet_workflow']
        )
        test_file = api.content.create(
            container=api.portal.get(),
            type='File',
            id='test-file',
        )
        self.assertEqual(
            api.content.get_state(test_file),
            'internal',
        )
        api.content.transition(
            obj=test_file,
            transition='hide',
        )

        # the following transition must move through the internal state
        api.content.transition(
            obj=test_file,
            to_state='internally_published',
        )
        self.assertEqual(
            api.content.get_state(test_file),
            'internally_published',
        )

    def test_get_view_constraints(self):
        """Test the constraints for deleting content."""
        from plone.api.exc import MissingParameterError
        request = self.layer['request']

        # When no parameters are given an error is raised
        with self.assertRaises(MissingParameterError):
            api.content.get_view()

        # name is required
        with self.assertRaises(MissingParameterError):
            api.content.get_view(
                context=self.blog,
                request=request,
            )

        # context is required
        with self.assertRaises(MissingParameterError):
            api.content.get_view(
                name='plone',
                request=request,
            )

        # request is required
        with self.assertRaises(MissingParameterError):
            api.content.get_view(
                name='plone',
                context=self.blog,
            )

    def test_get_view(self):
        """Test the view."""
        request = self.layer['request']

        view = api.content.get_view(
            name='plone',
            context=self.blog,
            request=request,
        )
        self.assertEqual(aq_base(view.context), aq_base(self.blog))
        self.assertEqual(view.__name__, 'plone')
        self.assertTrue(hasattr(view, 'getIcon'))

        # Try another standard view.
        view = api.content.get_view(
            name='plone_context_state',
            context=self.blog,
            request=request,
        )
        self.assertEqual(view.__name__, 'plone_context_state')
        self.assertEqual(aq_base(view.canonical_object()), aq_base(self.blog))

    def test_get_uuid(self):
        """Test getting a content item's UUID."""
        from plone.api.exc import MissingParameterError

        container = self.portal

        # The content item must be given as parameter
        with self.assertRaises(MissingParameterError):
            api.content.get_uuid()

        generator = getUtility(IUUIDGenerator)

        # Set the UUID and compare it with the one we get from our function
        # Dexterity
        container.invokeFactory('Dexterity Item', 'test-dexterity')
        item = container['test-dexterity']
        uuid1 = generator()
        IMutableUUID(item).set(uuid1)

        uuid2 = api.content.get_uuid(item)
        self.assertEqual(uuid1, uuid2)
        self.assertIsInstance(uuid2, str)

        if not HAS_PACONTENTYPES:
            container.invokeFactory('Document', 'test-archetype')
            document = container['test-archetype']
            uuid1 = generator()
            document._setUID(uuid1)

            uuid2 = api.content.get_uuid(document)
            self.assertEqual(uuid1, uuid2)
            self.assertIsInstance(uuid2, str)

    def test_get_view_view_not_found(self):
        """Test that error msg lists available views if a view is not found."""
        request = self.layer['request']
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError) as cm:
            api.content.get_view(
                name='foo',
                context=self.blog,
                request=request
            )

        self.maxDiff = None  # to see assert diff
        self.assertTrue(
            str(cm.exception).startswith(
                "Cannot find a view with name 'foo'.\n"
                "Available views are:\n"
                '\n'
            )
        )

        # This is just a sampling of views that should be present.
        # Test against only these rather than the full list. Otherwise, this
        # test has to maintain an up-to-date list of every view in Plone.
        should_be_theres = (
            "adapter",
            "authenticator",
            "checkDocument",
            "get_macros",
            "history",
            "plone",
            "plone_tools",
            "resource",
            "search",
            "sharing",
            "skin",
            "text-transform",
            "uuid",
            "view",
        )

        for should_be_there in should_be_theres:
            self.assertIn((should_be_there + '\n'), str(cm.exception))
