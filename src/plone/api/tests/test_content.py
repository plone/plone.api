"""Tests for plone.api.content."""

from Acquisition import aq_base
from OFS.CopySupport import CopyError
from OFS.event import ObjectWillBeMovedEvent
from OFS.interfaces import IObjectWillBeMovedEvent
from plone import api
from plone.api.content import _parse_object_provides_query
from plone.api.exc import MissingParameterError
from plone.api.tests.base import INTEGRATION_TESTING
from plone.app.contenttypes.interfaces import IFolder
from plone.app.linkintegrity.exceptions import LinkIntegrityNotificationException
from plone.app.textfield import RichTextValue
from plone.base.interfaces import INavigationRoot
from plone.indexer import indexer
from plone.uuid.interfaces import IMutableUUID
from plone.uuid.interfaces import IUUIDGenerator
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.ZCatalog.interfaces import IZCatalog
from unittest import mock
from zExceptions import BadRequest
from zope.component import getGlobalSiteManager
from zope.component import getUtility
from zope.container.contained import ContainerModifiedEvent
from zope.interface import alsoProvides
from zope.lifecycleevent import IObjectModifiedEvent
from zope.lifecycleevent import IObjectMovedEvent
from zope.lifecycleevent import modified
from zope.lifecycleevent import ObjectMovedEvent

import unittest


class TestPloneApiContent(unittest.TestCase):
    """Unit tests for content manipulation using plone.api."""

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
        self.portal = self.layer["portal"]

        self.blog = api.content.create(
            type="Link",
            id="blog",
            container=self.portal,
        )
        self.about = api.content.create(
            type="Folder",
            id="about",
            container=self.portal,
        )
        self.events = api.content.create(
            type="Folder",
            id="events",
            container=self.portal,
        )

        self.team = api.content.create(
            container=self.about,
            type="Document",
            id="team",
        )
        self.contact = api.content.create(
            container=self.about,
            type="Document",
            id="contact",
        )

        self.training = api.content.create(
            container=self.events,
            type="Event",
            id="training",
        )
        self.conference = api.content.create(
            container=self.events,
            type="Event",
            id="conference",
        )
        self.sprint = api.content.create(
            container=self.events,
            type="Event",
            id="sprint",
        )

        self.image = api.content.create(
            container=self.portal,
            type="Image",
            id="image",
        )

    def verify_intids(self):
        """Test that the intids are in order."""
        from zope.component import getUtility
        from zope.intid.interfaces import IIntIds

        intids = getUtility(IIntIds)
        broken_keys = [
            key
            for key in intids.ids
            if not self.portal.unrestrictedTraverse(key.path, None)
        ]
        obsolete_paths = [key.path for key in broken_keys]
        self.assertListEqual(obsolete_paths, [])

        # Objects used as keys with a hash can behave strangely.
        # I have seen this go wrong in a production site.
        weird_keys = [key for key in intids.ids if key not in intids.ids]
        weird_paths = [key.path for key in weird_keys]
        self.assertListEqual(weird_paths, [])

    def test_create_constraints(self):
        """Test the constraints when creating content."""
        from plone.api.exc import InvalidParameterError
        from plone.api.exc import MissingParameterError

        # This will definitely fail
        with self.assertRaises(MissingParameterError):
            api.content.create()

        # Check the constraints for the type container
        with self.assertRaises(MissingParameterError):
            api.content.create(
                type="Document",
                id="test-doc",
            )

        # Check the constraints for the type parameter
        container = mock.Mock()
        with self.assertRaises(MissingParameterError):
            api.content.create(
                container=container,
                id="test-doc",
            )

        # Check the constraints for id and title parameters
        with self.assertRaises(MissingParameterError):
            api.content.create(
                container=container,
                type="Document",
            )

        # Check the constraints for allowed types in the container
        container = self.events
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=container,
                type="foo",
                id="test-foo",
            )

        # Check the constraints for allowed types in the container if
        # the container is the portal
        container = self.portal
        with self.assertRaises(InvalidParameterError) as cm:
            api.content.create(
                container=container,
                type="foo",
                id="test-foo",
            )

        # Check if the underlying error message is included
        # in the InvalidParameterError message
        self.assertIn(
            "No such content type: foo",
            str(cm.exception),
        )

        # Check the constraints for allowed types in the container
        # Create a folder
        folder = api.content.create(
            container=container,
            type="Folder",
            id="test-folder",
        )
        assert folder

        # Constraint the allowed types
        ENABLED = 1
        if getattr(aq_base(folder), "setConstrainTypesMode", None):  # AT
            folder.setConstrainTypesMode(ENABLED)
            folder.setLocallyAllowedTypes(("News Item",))
        else:  # DX
            from plone.base.interfaces import ISelectableConstrainTypes

            constraints = ISelectableConstrainTypes(folder)
            constraints.setConstrainTypesMode(ENABLED)
            constraints.setLocallyAllowedTypes(("News Item",))

        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=folder,
                type="Document",
                id="test-doc",
            )

    def test_create_dexterity(self):
        """Test create dexterity."""
        container = self.portal

        # This section check for DX compatibility. The custom DX types defined
        # in plone.api are for Plone 4 compatibility.

        # Create a folder
        folder = api.content.create(
            container=container,
            type="Dexterity Folder",
            id="test-folder",
        )
        assert folder
        self.assertEqual(folder.id, "test-folder")
        self.assertEqual(folder.portal_type, "Dexterity Folder")

        # Create an item
        page = api.content.create(
            container=folder,
            type="Dexterity Item",
            id="test-item",
        )
        assert page
        self.assertEqual(page.id, "test-item")
        self.assertEqual(page.portal_type, "Dexterity Item")

        # Create an item with a title and without an id
        page = api.content.create(
            container=folder,
            type="Dexterity Item",
            title="Test id generated",
        )
        assert page
        self.assertEqual(page.id, "test-id-generated")
        self.assertEqual(page.Title(), "Test id generated")
        self.assertEqual(page.portal_type, "Dexterity Item")

        # Try to create another item with same id, this should fail
        with self.assertRaises(BadRequest):
            api.content.create(
                container=folder,
                type="Dexterity Item",
                id="test-item",
            )
        self.verify_intids()

    def test_create_content(self):
        """Test create content."""
        container = self.portal

        # This section below is either AT (Plone < 5) or DX (Plone >= 5)
        # We use Products.ATContentTypes in Plone 4 or plone.app.contenttypes
        # in Plone 5

        # Create a folder
        folder = api.content.create(
            container=container,
            type="Folder",
            id="test-folder",
        )
        assert folder
        self.assertEqual(folder.id, "test-folder")
        self.assertEqual(folder.portal_type, "Folder")

        # Create a document
        page = api.content.create(
            container=folder,
            type="Document",
            id="test-document",
        )
        assert page
        self.assertEqual(page.id, "test-document")
        self.assertEqual(page.portal_type, "Document")

        # Create a document with a title and without an id
        page = api.content.create(
            container=folder,
            type="Document",
            title="Test id generated",
        )
        assert page
        self.assertEqual(page.id, "test-id-generated")
        self.assertEqual(page.Title(), "Test id generated")
        self.assertEqual(page.portal_type, "Document")

        # Try to create another page with same id, this should fail
        with self.assertRaises(BadRequest):
            api.content.create(
                container=folder,
                type="Document",
                id="test-document",
            )
        self.verify_intids()

    def test_create_with_safe_id(self):
        """Test the content creating with safe_id mode."""
        container = self.portal

        first_page = api.content.create(
            container=container,
            type="Document",
            id="test-document",
            safe_id=True,
        )
        assert first_page
        self.assertEqual(first_page.id, "test-document")
        self.assertEqual(first_page.portal_type, "Document")

        # Second page is created with non-conflicting id
        second_page = api.content.create(
            container=container,
            type="Document",
            id="test-document",
            safe_id=True,
        )
        assert second_page
        self.assertEqual(second_page.id, "test-document-1")
        self.assertEqual(second_page.portal_type, "Document")

    def test_create_raises_unicodedecodeerror(self):
        """Test that the create method raises UnicodeDecodeErrors correctly."""
        site = getGlobalSiteManager()
        unicode_exception_message = "This is a fake unicode error"

        # register a title indexer that will force a UnicodeDecodeError
        # during content reindexing
        @indexer(IFolder, IZCatalog)
        def force_unicode_error(object):
            raise UnicodeDecodeError(
                "ascii",
                b"x",
                1,
                5,
                unicode_exception_message,
            )

        site.registerAdapter(factory=force_unicode_error, name="Title")

        def unregister_indexer():
            site.unregisterAdapter(factory=force_unicode_error, name="Title")

        self.addCleanup(unregister_indexer)

        with self.assertRaises(UnicodeDecodeError) as ude:
            api.content.create(
                type="Folder",
                id="test-unicode-folder",
                container=self.portal,
            )

        # check that the exception is the one we raised
        self.assertEqual(ude.exception.reason, unicode_exception_message)

    def test_create_at_with_title_in_request(self):
        """Test that content gets created with the correct title.

        even if request.form['title'] already exists and has a different value.
        This can occur, for example, when adding a Plone with an enabled
        product that creates a site structure. In that case, the 'title'
        would be that of the portal.
        Only AT content types are affected, due to content.processForm.
        """
        leaked_title = "This should not be set on content items"
        self.layer["request"].form["title"] = leaked_title

        container = self.portal

        # Create a folder
        folder = api.content.create(
            container=container,
            type="Folder",
            title="Test folder",
        )

        self.assertEqual(folder.title, "Test folder")

        # Create a document
        page = api.content.create(
            container=folder,
            type="Document",
            title="Test document",
        )

        self.assertEqual(page.title, "Test document")

    def test_create_collection(self):
        """Test create a Collection."""
        collection = api.content.create(
            container=self.portal,
            type="Collection",
            title="Mandelbrot set",
            description="Image gallery of a zoom sequence",
            query=[
                {
                    "i": "Type",
                    "o": "plone.app.querystring.operation.string.is",
                    "v": ["Image"],
                },
            ],
        )
        self.assertEqual(collection.Title(), "Mandelbrot set")

    def test_create_event(self):
        """Test create a event."""
        import datetime

        today = datetime.datetime.now()
        tomorrow = today + datetime.timedelta(days=1)
        event = api.content.create(
            container=self.portal,
            type="Event",
            title="My event",
            start=today,
            end=tomorrow,
        )
        self.assertEqual(event.start, today)
        self.assertEqual(event.end, tomorrow)
        results = api.content.find(Title="My event")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].start, today)
        self.assertEqual(results[0].end, tomorrow)

    def test_get_constraints(self):
        """Test the constraints when content is fetched with get."""
        # Path and UID parameter can not be given together
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError):
            api.content.get(
                path="/",
                UID="dummy",
            )

        # Either a path or UID must be given
        from plone.api.exc import MissingParameterError

        with self.assertRaises(MissingParameterError):
            api.content.get()

    def test_get(self):
        """Test the getting of content in various ways."""
        # Test getting the about folder by path and UID
        about_by_path = api.content.get("/about")
        about_by_uid = api.content.get(UID=self.about.UID())
        self.assertEqual(self.about, about_by_path)
        self.assertEqual(self.about, about_by_uid)

        # Test getting the team document by path and UID
        team_by_path = api.content.get("/about/team")
        team_by_uid = api.content.get(UID=self.team.UID())
        self.assertEqual(self.team, team_by_path)
        self.assertEqual(self.team, team_by_uid)

        # Test getting the team document by path that has portal id included
        team_by_path = api.content.get(
            f"/{self.portal.getId()}/about/team",
        )
        self.assertEqual(self.team, team_by_path)

        # Test getting an non-existing item by path and UID
        self.assertFalse(api.content.get("/spam/ham"))
        self.assertFalse(api.content.get(UID="bacon"))

        # Test getting a non-existing subfolder by path
        self.assertFalse(api.content.get("/about/spam"))

        # Test get will always return a content
        # Title is a method
        self.assertIsNone(api.content.get("/about/team/Title"))
        # title is an attribute
        self.assertIsNone(api.content.get("/about/team/title"))

    def test_get_of_content_in_inaccessible_container(self):
        """Test getting items in a inaccessible container.
        Worked in Plone 5.1 but raised Unauthorized since 5.2."""
        api.content.transition(obj=self.team, transition="publish")
        with api.env.adopt_roles(["Member"]):
            team_by_path = api.content.get("/about/team")
            self.assertEqual(self.team, team_by_path)
            team_by_uid = api.content.get(UID=self.team.UID())
            self.assertEqual(self.team, team_by_uid)

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
        nucontact = api.content.move(source=self.contact, id="nu-contact")
        assert (
            container["about"]["nu-contact"]
            and container["about"]["nu-contact"] == nucontact
        )
        assert "contact" not in container["about"].keys()

        # Move team page to portal root
        team = api.content.move(source=self.team, target=container)
        assert container["team"] and container["team"] == team
        assert "team" not in container["about"].keys()

        # When moving objects we can change the id
        team = container["team"]
        ourteam = api.content.move(
            source=team,
            target=self.about,
            id="our-team",
        )
        assert (
            container["about"]["our-team"] and container["about"]["our-team"] == ourteam
        )
        assert "team" not in container.keys()

        # Test with safe_id option when moving content
        api.content.create(
            container=self.about,
            type="Link",
            id="link-to-blog",
        )
        linktoblog1 = api.content.move(
            source=self.blog,
            target=self.about,
            id="link-to-blog",
            safe_id=True,
        )
        assert (
            container["about"]["link-to-blog-1"]
            and container["about"]["link-to-blog-1"] == linktoblog1
        )
        assert "link-to-blog" not in container.keys()

        api.content.move(source=self.conference, id="conference-renamed")
        self.assertEqual(self.conference.id, "conference-renamed")

        # Move folderish object
        about = api.content.move(
            source=container.about,
            target=container.events,
        )
        assert container["events"]["about"] and container["events"]["about"] == about
        self.verify_intids()

    def test_move_no_move_if_target_is_source_parent(self):
        """Test that trying to move an object to its parent is a noop."""
        target = self.contact.aq_parent
        with mock.patch.object(target, "manage_pasteObjects"):
            api.content.move(
                source=self.contact,
                target=target,
            )

            self.assertFalse(target.manage_pasteObjects.called)

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
        nucontact = api.content.rename(obj=self.contact, new_id="nu-contact")
        assert (
            container["about"]["nu-contact"]
            and container["about"]["nu-contact"] == nucontact
        )
        assert "contact" not in container["about"].keys()

        self.assertCountEqual(
            firedEvents,
            [
                ObjectMovedEvent,
                ObjectWillBeMovedEvent,
                ContainerModifiedEvent,
            ],
        )
        sm.unregisterHandler(recordEvent, (IObjectWillBeMovedEvent,))
        sm.unregisterHandler(recordEvent, (IObjectMovedEvent,))
        sm.unregisterHandler(recordEvent, (IObjectModifiedEvent,))

        # Test with safe_id option when moving content
        api.content.create(
            container=self.about,
            type="Link",
            id="link-to-blog",
        )
        linktoblog1 = api.content.rename(
            obj=container["about"]["link-to-blog"],
            new_id="link-to-blog",
            safe_id=True,
        )
        assert (
            container["about"]["link-to-blog-1"]
            and container["about"]["link-to-blog-1"] == linktoblog1
        )
        assert "link-to-blog" not in container.keys()

        # Rename to existing id
        api.content.create(
            container=self.about,
            type="Link",
            id="link-to-blog",
        )

        with self.assertRaises(CopyError):
            api.content.rename(
                obj=container["about"]["link-to-blog"],
                new_id="link-to-blog-1",
            )
        linktoblog11 = api.content.rename(
            obj=container["about"]["link-to-blog"],
            new_id="link-to-blog-1",
            safe_id=True,
        )
        assert (
            container["about"]["link-to-blog-1-1"]
            and container["about"]["link-to-blog-1-1"] == linktoblog11
        )
        assert "link-to-blog" not in container.keys()

    def test_rename_same_id(self):
        api.content.rename(obj=self.contact, new_id=self.contact.getId())

    def test_rename_same_folder(self):
        # When renaming a folderish item with safe_id=True, and there is
        # already an existing folderish item with that id, it should choose
        # a new name.

        events = self.portal["events"]
        about = self.portal["about"]
        api.content.rename(
            obj=events,
            new_id="about",
            safe_id=True,
        )

        assert self.portal["about"]
        assert self.portal["about-1"]
        assert self.portal["about"].aq_base is about.aq_base
        assert self.portal["about-1"].aq_base is events.aq_base

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
        assert container["team"] and container["team"] == team
        assert (
            container["about"]["team"] and container["about"]["team"] != team
        )  # old content still available

        # When copying objects we can change the id
        ourteam = api.content.copy(
            source=self.team,
            target=self.about,
            id="our-team",
        )
        assert (
            container["about"]["our-team"] and container["about"]["our-team"] == ourteam
        )

        # When copying without target parameter should take source parent
        api.content.copy(source=self.team, id="our-team-no-target")
        assert container["about"]["our-team-no-target"]

        # Test the safe_id option when moving content
        api.content.create(
            container=self.about,
            type="Link",
            id="link-to-blog",
        )

        linktoblog1 = api.content.copy(
            source=self.blog,
            target=self.about,
            id="link-to-blog",
            safe_id=True,
        )
        assert (
            container["about"]["link-to-blog-1"]
            and container["about"]["link-to-blog-1"] == linktoblog1
        )

        # Copy folderish content under target
        about = api.content.copy(
            source=container.about,
            target=container.events,
        )
        assert container["events"]["about"] and container["events"]["about"] == about

        # When copying with safe_id=True, the prior created item should not be
        # renamed, and the copied item should have a sane postfix

        # Create a products folder
        products = api.content.create(
            type="Folder",
            id="products",
            container=self.portal,
        )

        # Create a item inside the products folder
        item = api.content.create(
            container=products,
            type="Document",
            id="item",
        )

        api.content.copy(source=item, id="item", safe_id=True)

        assert container["products"]["item-1"]
        assert container["products"]["item"]

        # When copying with safe_id=True, the created bargain with the id=item
        # should not be renamed, and the item copied from the products folder
        # should have a sane postfix.
        # The item in the the products folder should still exist.

        # Create a second folder named bargains
        bargains = api.content.create(
            type="Folder",
            id="bargains",
            container=self.portal,
        )

        # Create a bargain inside the bargains folder with the id="item"
        bargain = api.content.create(
            type="Document",
            id="item",
            container=bargains,
        )
        api.content.copy(
            source=item,
            target=bargains,
            id="item",
            safe_id=True,
        )

        assert container["bargains"]["item-1"]
        assert container["bargains"]["item"]
        assert container["bargains"]["item"].aq_base is bargain.aq_base
        assert container["products"]["item"]

    def test_copy_same_id(self):
        obj = self.contact

        # Using the same id should fail
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError):
            api.content.copy(obj, obj.__parent__, obj.id)

        # Using safe_id=True should work
        api.content.copy(obj, obj.__parent__, obj.id, safe_id=True)

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
        self.assertNotIn("contact", container["about"].keys())

    def test_delete_multiple(self):
        """Test deleting multiple content items."""

        container = self.portal
        api.content.copy(source=container["about"], target=container)
        api.content.copy(source=container["about"], target=container["events"])

        api.content.delete(
            objects=[
                container["copy_of_about"],
                container["events"]["about"],
            ],
        )
        self.assertNotIn("copy_of_about", container)
        self.assertNotIn("about", container["events"])

    def test_delete_no_objs(self):
        # Check that we allow passing in an empty list of objects.
        api.content.delete(obj=None, objects=[])

    def test_delete_ignore_linkintegrity(self):
        """Test deleting a content item with a link pointed at it."""
        self._set_text(self.team, '<a href="contact">contact</a>')
        # Delete the contact page
        api.content.delete(self.contact, check_linkintegrity=False)
        self.assertNotIn("contact", self.portal["about"].keys())

    def test_delete_check_linkintegrity(self):
        """Test deleting a content item with a link pointed at it."""
        self._set_text(self.team, '<a href="contact">contact</a>')
        # Delete the contact page
        with self.assertRaises(LinkIntegrityNotificationException):
            api.content.delete(self.contact)
        self.assertIn("contact", self.portal["about"].keys())

    def test_delete_multiple_check_linkintegrity(self):
        """Test deleting multiple item with linkintegrity-breaches."""
        self._set_text(self.team, '<a href="../about/contact">contact</a>')
        self._set_text(self.training, '<a href="../blog">contact</a>')
        # Delete the contact page
        with self.assertRaises(LinkIntegrityNotificationException):
            api.content.delete(objects=[self.blog, self.contact])
        self.assertIn("contact", self.portal["about"].keys())
        self.assertIn("blog", self.portal.keys())

    def test_delete_multiple_ignore_linkintegrity(self):
        """Test deleting multiple items ignoring linkintegrity-breaches."""
        self._set_text(self.team, '<a href="../about/contact">contact</a>')
        self._set_text(self.training, '<a href="../blog">contact</a>')
        # Delete linked pages
        api.content.delete(
            objects=[self.blog, self.contact],
            check_linkintegrity=False,
        )
        self.assertNotIn("contact", self.portal["about"].keys())
        self.assertNotIn("blog", self.portal.keys())

    def test_delete_with_internal_breaches(self):
        """Test deleting multiple with internal linkintegrity breaches."""
        self._set_text(self.team, '<a href="../about/contact">contact</a>')
        self._set_text(self.training, '<a href="../blog">contact</a>')
        # Deleting pages with unresolved breaches throws an exception
        with self.assertRaises(LinkIntegrityNotificationException):
            api.content.delete(objects=[self.blog, self.about])
        self.assertIn("about", self.portal.keys())
        self.assertIn("blog", self.portal.keys())
        self.assertIn("training", self.portal["events"].keys())

    def test_delete_with_resolved_internal_breaches(self):
        """Test deleting multiple with internal linkintegrity breaches."""
        self._set_text(self.team, '<a href="../about/contact">contact</a>')
        self._set_text(self.training, '<a href="../blog">contact</a>')
        # Deleting pages with resolved breaches throws no exception
        api.content.delete(objects=[self.blog, self.training, self.about])
        self.assertNotIn("about", self.portal.keys())
        self.assertNotIn("blog", self.portal.keys())
        self.assertNotIn("training", self.portal["events"].keys())

    def _set_text(self, obj, text):
        obj.text = RichTextValue(text, "text/html", "text/x-html-safe")
        modified(obj)

    def test_find(self):
        """Test the finding of content in various ways."""

        # Find documents
        documents = api.content.find(portal_type="Document")
        self.assertEqual(len(documents), 2)

    def test_untrestricted_find(self):
        """Test the finding of content in with unrestricted search."""

        # Search as Anonymous user
        from plone.app.testing import logout

        logout()

        # Find documents (unrestricted)
        documents = api.content.find(portal_type="Document", unrestricted=True)
        self.assertEqual(len(documents), 2)

        # Find documents (restricted)
        documents = api.content.find(portal_type="Document")
        self.assertEqual(len(documents), 0)

    def test_find_empty_query(self):
        """Make sure an empty query yields no results"""

        documents = api.content.find()
        self.assertEqual(len(documents), 0)

    def test_find_invalid_indexes(self):
        """Make sure invalid indexes yield no results"""

        # All invalid indexes yields no results
        documents = api.content.find(invalid_index="henk")
        self.assertEqual(len(documents), 0)

        # But at least one valid index does.
        documents = api.content.find(
            invalid_index="henk",
            portal_type="Document",
        )
        self.assertEqual(len(documents), 2)

    def test_find_context(self):
        # Find documents in context
        documents = api.content.find(
            context=self.portal.about,
            portal_type="Document",
        )
        self.assertEqual(len(documents), 2)
        documents = api.content.find(
            context=self.portal.events,
            portal_type="Document",
        )
        self.assertEqual(len(documents), 0)

    def test_find_depth(self):
        # Limit search depth from portal root
        documents = api.content.find(depth=2, portal_type="Document")
        self.assertEqual(len(documents), 2)
        documents = api.content.find(depth=1, portal_type="Document")
        self.assertEqual(len(documents), 0)

        # Limit search depth with explicit context
        documents = api.content.find(
            context=self.portal.about,
            depth=1,
            portal_type="Document",
        )
        self.assertEqual(len(documents), 2)
        documents = api.content.find(
            context=self.portal.about,
            depth=0,
            portal_type="Document",
        )
        self.assertEqual(len(documents), 0)

        # Limit search depth with explicit path
        documents = api.content.find(
            path="/".join(self.portal.about.getPhysicalPath()),
            depth=1,
            portal_type="Document",
        )
        self.assertEqual(len(documents), 2)
        documents = api.content.find(
            path="/".join(self.portal.about.getPhysicalPath()),
            depth=0,
            portal_type="Document",
        )
        self.assertEqual(len(documents), 0)
        documents = api.content.find(
            path="/".join(self.portal.events.getPhysicalPath()),
            depth=1,
            portal_type="Document",
        )
        self.assertEqual(len(documents), 0)

    def test_find_interface(self):
        # Find documents by interface or it's identifier
        identifier = IFolder.__identifier__
        brains = api.content.find(object_provides=identifier)
        by_identifier = [x.getObject() for x in brains]

        brains = api.content.find(object_provides=IFolder)
        by_interface = [x.getObject() for x in brains]

        self.assertEqual(by_identifier, by_interface)

    def test_find_interface_dict(self):
        # Find documents by interface combined with 'and'

        alsoProvides(self.portal.events, INavigationRoot)
        self.portal.events.reindexObject(idxs=["object_provides"])

        # standard catalog query using identifiers
        brains = api.content.find(
            object_provides={
                "query": [
                    IFolder.__identifier__,
                    INavigationRoot.__identifier__,
                ],
                "operator": "and",
            },
        )

        self.assertEqual(len(brains), 1)

        # plone.api query using interfaces
        brains = api.content.find(
            object_provides={
                "query": [IFolder, INavigationRoot],
                "operator": "and",
            },
        )
        self.assertEqual(len(brains), 1)

    def test_find_interface_dict__include_not_query(self):
        """Check if not query in object_provides is functional."""

        brains_all = api.content.find(
            object_provides={"query": IFolder.__identifier__},
        )

        alsoProvides(self.portal.events, INavigationRoot)
        self.portal.events.reindexObject(idxs=["object_provides"])

        brains = api.content.find(
            object_provides={
                "query": IFolder.__identifier__,
                "not": INavigationRoot.__identifier__,
            },
        )
        self.assertEqual(len(brains_all) - len(brains), 1)

    def test_find_interface_dict__all_options(self):
        """Check for all options in a object_provides query are correctly
        transformed.
        """
        parser = _parse_object_provides_query

        self.assertDictEqual(
            parser({"query": IFolder}),
            {"query": [IFolder.__identifier__], "operator": "or"},
        )

        self.assertDictEqual(
            parser(
                {
                    "query": [IFolder, INavigationRoot.__identifier__],
                    "operator": "and",
                },
            ),
            {
                "query": [IFolder.__identifier__, INavigationRoot.__identifier__],
                "operator": "and",
            },
        )

        self.assertDictEqual(
            parser({"not": IFolder}),
            {"not": [IFolder.__identifier__]},
        )

        self.assertDictEqual(
            parser({"not": [IFolder, INavigationRoot.__identifier__]}),
            {"not": [IFolder.__identifier__, INavigationRoot.__identifier__]},
        )

        self.assertDictEqual(
            parser({"not": IFolder}),
            {"not": [IFolder.__identifier__]},
        )

        self.assertDictEqual(
            parser({"query": IFolder, "operator": "and", "not": INavigationRoot}),
            {
                "query": [IFolder.__identifier__],
                "operator": "and",
                "not": [INavigationRoot.__identifier__],
            },
        )

    def test_find_dict(self):
        # Pass arguments using dict
        path = "/".join(self.portal.about.getPhysicalPath())

        query = {
            "portal_type": "Document",
            "path": {"query": path, "depth": 2},
        }
        documents = api.content.find(**query)
        self.assertEqual(len(documents), 2)

        query = {
            "portal_type": "Document",
            "path": {"query": path, "depth": 0},
        }
        documents = api.content.find(**query)
        self.assertEqual(len(documents), 0)

        # This is a bit awkward, but it is nice if this does not crash.
        query = {
            "depth": 2,
            "portal_type": "Document",
            "path": {"query": path},
        }
        documents = api.content.find(**query)
        self.assertEqual(len(documents), 2)

        path = "/".join(self.portal.events.getPhysicalPath())
        query = {
            "depth": 2,
            "portal_type": "Document",
            "path": {"query": path},
        }
        documents = api.content.find(**query)
        self.assertEqual(len(documents), 0)

    def test_find_parse_object_provides_query(self):
        parse = api.content._parse_object_provides_query

        # single interface
        self.assertDictEqual(
            parse(IFolder),
            {
                "query": [IFolder.__identifier__],
                "operator": "or",
            },
        )
        # single identifier
        self.assertDictEqual(
            parse(IFolder.__identifier__),
            {
                "query": [IFolder.__identifier__],
                "operator": "or",
            },
        )
        # multiple interfaces/identifiers (mixed as list)
        self.assertDictEqual(
            parse([INavigationRoot, IFolder.__identifier__]),
            {
                "query": [
                    INavigationRoot.__identifier__,
                    IFolder.__identifier__,
                ],
                "operator": "or",
            },
        )
        # multiple interfaces/identifiers (mixed as tuple)
        self.assertDictEqual(
            parse((INavigationRoot, IFolder.__identifier__)),
            {
                "query": [
                    INavigationRoot.__identifier__,
                    IFolder.__identifier__,
                ],
                "operator": "or",
            },
        )
        # full blown query - interfaces/identifiers mixed
        self.assertDictEqual(
            parse(
                {
                    "query": [INavigationRoot, IFolder.__identifier__],
                    "operator": "and",
                }
            ),
            {
                "query": [
                    INavigationRoot.__identifier__,
                    IFolder.__identifier__,
                ],
                "operator": "and",
            },
        )

    def test_get_state(self):
        """Test retrieving the workflow state of a content item."""
        # This should fail because an content item is mandatory
        from plone.api.exc import MissingParameterError

        with self.assertRaises(MissingParameterError):
            api.content.get_state()

        review_state = api.content.get_state(obj=self.blog)
        self.assertEqual(review_state, "private")

    def test_get_state_default_value(self):
        """Test passing in a default value."""
        # A WorkflowException is raise if no workflow is defined for the obj.
        # This is normally the case for Images and Files.
        with self.assertRaises(WorkflowException):
            review_state = api.content.get_state(obj=self.image)

        default = "my default value"
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
            api.content.transition(transition="publish")

        with self.assertRaises(InvalidParameterError):
            api.content.transition(
                obj=mock.Mock(),
                transition="publish",
                to_state="published",
            )

        api.content.transition(obj=self.blog, transition="publish")
        review_state = api.content.get_state(obj=self.blog)
        self.assertEqual(review_state, "published")

        # This should fail because the transition doesn't exist
        with self.assertRaises(InvalidParameterError) as cm:
            api.content.transition(
                transition="foo",
                obj=self.blog,
            )

        self.maxDiff = None  # to see assert diff
        self.assertMultiLineEqual(
            str(cm.exception),
            "Invalid transition 'foo'.\n"
            "Valid transitions are:\n"
            "reject\n"
            "retract",
        )

        # change the workflow of a document so that there is no transition
        # that goes directly from one state to another
        portal_workflow = api.portal.get_tool("portal_workflow")
        portal_workflow._chains_by_type["File"] = tuple(
            ["intranet_workflow"],
        )
        test_file = api.content.create(
            container=api.portal.get(),
            type="File",
            id="test-file",
        )
        self.assertEqual(
            api.content.get_state(test_file),
            "internal",
        )
        api.content.transition(
            obj=test_file,
            transition="hide",
        )

        # the following transition must move through the internal state
        api.content.transition(
            obj=test_file,
            to_state="internally_published",
        )
        self.assertEqual(
            api.content.get_state(test_file),
            "internally_published",
        )

    def test_disable_roles_acquisition(self):
        """Test disabling local roles acquisition."""
        # This should fail because an content item is mandatory
        from plone.api.exc import MissingParameterError

        with self.assertRaises(MissingParameterError):
            api.content.disable_roles_acquisition()

        api.content.disable_roles_acquisition(obj=self.blog)
        blog_ac_flag = getattr(self.blog, "__ac_local_roles_block__", None)
        self.assertTrue(blog_ac_flag)

    def test_enable_roles_acquisition(self):
        """Test enabling local roles acquisition."""
        # This should fail because an content item is mandatory
        from plone.api.exc import MissingParameterError

        with self.assertRaises(MissingParameterError):
            api.content.enable_roles_acquisition()

        # As __ac_local_roles_block__ is None by default, we have to set it,
        # before we can test the enabling method.
        self.blog.__ac_local_roles_block__ = 1

        api.content.enable_roles_acquisition(obj=self.blog)
        blog_ac_flag = getattr(self.blog, "__ac_local_roles_block__", None)
        self.assertFalse(blog_ac_flag)

    def test_get_view_constraints(self):
        """Test the constraints for deleting content."""
        from plone.api.exc import MissingParameterError

        request = self.layer["request"]

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
                name="plone",
                request=request,
            )

    def test_get_view(self):
        """Test the view."""
        request = self.layer["request"]

        view = api.content.get_view(
            name="plone",
            context=self.blog,
            request=request,
        )
        self.assertEqual(aq_base(view.context), aq_base(self.blog))
        self.assertEqual(view.__name__, "plone")
        self.assertTrue(hasattr(view, "toLocalizedTime"))
        self.assertTrue(hasattr(view, "isDefaultPageInFolder"))

        # Try another standard view.
        view = api.content.get_view(
            name="plone_context_state",
            context=self.blog,
            request=request,
        )
        self.assertEqual(view.__name__, "plone_context_state")
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
        container.invokeFactory("Dexterity Item", "test-dexterity")
        item = container["test-dexterity"]
        uuid1 = generator()
        IMutableUUID(item).set(uuid1)

        uuid2 = api.content.get_uuid(item)
        self.assertEqual(uuid1, uuid2)
        self.assertIsInstance(uuid2, str)

    def test_get_view_view_not_found(self):
        """Test that error msg lists available views if a view is not found."""
        request = self.layer["request"]
        from plone.api.exc import InvalidParameterError

        with self.assertRaises(InvalidParameterError) as cm:
            api.content.get_view(
                name="foo",
                context=self.blog,
                request=request,
            )

        self.maxDiff = None  # to see assert diff
        self.assertTrue(
            str(cm.exception).startswith(
                "Cannot find a view with name 'foo'.\n" "Available views are:\n" "\n",
            ),
        )

        # This is just a sampling of views that should be present.
        # Test against only these rather than the full list. Otherwise, this
        # test has to maintain an up-to-date list of every view in Plone.
        should_be_theres = (
            "adapter",
            "authenticator",
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
            self.assertIn((should_be_there + "\n"), str(cm.exception))

    def test_get_path_absolute(self):
        """Test getting the path of a content object with relative parameter set to False."""
        from plone.api.exc import InvalidParameterError

        portal = self.layer["portal"]

        # Test portal root
        self.assertEqual(
            api.content.get_path(portal), "/plone"  # This assumes default Plone site id
        )

        # Test folder structure
        folder = api.content.create(container=portal, type="Folder", id="test-folder")
        self.assertEqual(api.content.get_path(folder), "/plone/test-folder")

        # Test nested content
        document = api.content.create(
            container=folder, type="Document", id="test-document"
        )
        self.assertEqual(
            api.content.get_path(document), "/plone/test-folder/test-document"
        )

        # Test invalid object
        invalid_obj = object()
        with self.assertRaises(InvalidParameterError):
            api.content.get_path(invalid_obj)
        self.assertRaisesRegex(
            InvalidParameterError,
            r"^Cannot get path of object <object object at 0x[0-9a-f]+>$",
        )

    def test_get_path_relative(self):
        from plone.api.exc import InvalidParameterError

        portal = self.layer["portal"]

        # Test portal root
        self.assertEqual(api.content.get_path(portal, relative=True), "")

        # Test folder structure
        folder = api.content.create(container=portal, type="Folder", id="test-folder")
        self.assertEqual(api.content.get_path(folder, relative=True), "test-folder")

        # Test nested content
        document = api.content.create(
            container=folder, type="Document", id="test-document"
        )
        self.assertEqual(
            api.content.get_path(document, relative=True),
            "test-folder/test-document",
        )

        # Test object outside portal
        class FauxObject:
            def getPhysicalPath(self):
                return ("", "foo", "bar")

        outside_obj = FauxObject()
        with self.assertRaises(InvalidParameterError) as cm:
            api.content.get_path(outside_obj, relative=True)
        self.assertIn("Object not in portal path", str(cm.exception))

    def test_iter_ancestors_required_parameter(self):
        """Test that iter_ancestors requires an obj parameter"""
        with self.assertRaises(MissingParameterError):
            api.content.iter_ancestors()

    def test_iter_ancestors(self):
        """Test iterating over all the ancestors until the portal root"""
        self.assertTupleEqual(
            tuple(api.content.iter_ancestors(self.team)), (self.about, self.portal)
        )

    def test_iter_ancestors_deep(self):
        """Test iterating over all the ancestors of the acquisition chain"""
        app = self.layer["app"]
        self.assertTupleEqual(
            tuple(api.content.iter_ancestors(self.team, stop_at=False)),
            (self.about, self.portal, app, app.aq_parent),
        )

    def test_iter_ancestors_stop_at(self):
        """Test iterating over all the ancestors until a specific object"""
        app = self.layer["app"]
        self.assertTupleEqual(
            tuple(api.content.iter_ancestors(self.team, stop_at=app)),
            (self.about, self.portal, app),
        )

    def test_iter_ancestors_with_interface(self):
        """Test iterating over all the ancestors with an interface filter"""
        self.assertTupleEqual(
            tuple(
                api.content.iter_ancestors(
                    self.team, interface=IFolderish, stop_at=False
                )
            ),
            (self.about, self.portal),
        )

    def test_iter_ancestors_with_function(self):
        """Test iterating over all the ancestors with a function filter"""
        self.assertTupleEqual(
            tuple(
                api.content.iter_ancestors(
                    self.team, function=lambda x: x.id == "about"
                )
            ),
            (self.about,),
        )

    def test_iter_ancestors_with_both_filters(self):
        """Test getting all parents with both filters"""
        self.assertTupleEqual(
            tuple(
                api.content.iter_ancestors(
                    self.sprint,
                    interface=IFolderish,
                    function=lambda x: x.id == "events",
                )
            ),
            (self.events,),
        )

    def test_iter_ancestors_for_portal(self):
        """Test iterating over all the ancestors of the portal"""
        self.assertTupleEqual(tuple(api.content.iter_ancestors(self.portal)), ())

    def test_iter_ancestors_bogus_stop_at(self):
        """Check that when we pass to the ``stop_at`` parameter something
        that is not in the acquisition chain, we raise an error."""
        with self.assertRaises(api.exc.InvalidParameterError) as cm:
            tuple(api.content.iter_ancestors(self.team, stop_at=self.sprint))

        self.assertEqual(
            str(cm.exception),
            (
                "The object <Event at /plone/events/sprint> "
                "is not in the acquisition chain of <Document at /plone/about/team>"
            ),
        )

    def test_iter_ancestors_not_acquisition_aware_object(self):
        """Test that iter_ancestors requires an obj parameter"""
        self.assertTupleEqual(
            tuple(api.content.iter_ancestors(object(), stop_at=False)), ()
        )

    def test_get_closest_ancestor_required_parameter(self):
        """Test that get_closest_ancestor requires an obj parameter"""
        with self.assertRaises(MissingParameterError):
            api.content.get_closest_ancestor()

    def test_get_closest_ancestor(self):
        """Test getting the closest ancestor of an object"""
        self.assertEqual(api.content.get_closest_ancestor(self.team), self.about)

    def test_get_closest_ancestor_with_interface(self):
        """Test getting the closest ancestor of an object with an interface filter"""
        self.assertEqual(
            api.content.get_closest_ancestor(self.team, interface=IFolderish),
            self.about,
        )

    def test_get_closest_ancestor_with_function(self):
        """Test getting the closest ancestor of an object with a function filter"""
        self.assertEqual(
            api.content.get_closest_ancestor(
                self.team, function=lambda x: x.id == "about"
            ),
            self.about,
        )

    def test_get_closest_ancestor_with_both_filters(self):
        """Test getting the closest ancestor of an object with both filters"""
        self.assertEqual(
            api.content.get_closest_ancestor(
                self.sprint,
                interface=IFolderish,
                function=lambda x: x.id == "events",
            ),
            self.events,
        )

    def test_get_closest_ancestor_for_portal(self):
        """Test getting the closest ancestor of the portal"""
        self.assertIsNone(api.content.get_closest_ancestor(self.portal))

    def test_get_closest_ancestor_bogus_stop_at(self):
        """Check that when we pass to the ``stop_at`` parameter something
        that is not in the acquisition chain, we raise an error."""
        with self.assertRaises(api.exc.InvalidParameterError) as cm:
            api.content.get_closest_ancestor(self.team, stop_at=self.sprint)

        self.assertEqual(
            str(cm.exception),
            (
                "The object <Event at /plone/events/sprint> "
                "is not in the acquisition chain of <Document at /plone/about/team>"
            ),
        )

    def test_get_closest_ancestor_not_acquisition_aware_object(self):
        """Test that get_closest_ancestor requires an obj parameter"""
        self.assertIsNone(api.content.get_closest_ancestor(object(), stop_at=False))
