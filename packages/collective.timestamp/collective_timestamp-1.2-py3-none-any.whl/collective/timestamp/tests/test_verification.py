# -*- coding: utf-8 -*-

from collective.timestamp.browser.viewlet import TimestampViewlet
from collective.timestamp.interfaces import ITimeStamper
from collective.timestamp.testing import COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class TestVerification(unittest.TestCase):

    layer = COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.document = api.content.create(
            container=self.portal,
            type="Document",
            id="my-document",
        )
        self.file = api.content.create(
            container=self.portal,
            type="File",
            id="my-file",
        )

    def test_viewlet(self):
        logout()
        viewlet = TimestampViewlet(self.document, self.request, None)
        with self.assertRaises(TypeError):
            viewlet.available()
        viewlet = TimestampViewlet(self.file, self.request, None)
        self.assertFalse(viewlet.available())
        self.file.file = NamedBlobFile(data=b"file data", filename="file.txt")
        self.assertFalse(viewlet.available())
        handler = ITimeStamper(self.file)
        handler.timestamp()
        self.assertTrue(viewlet.available())
        viewlet.update()
        html = viewlet.render()
        self.assertIn("svg", html)

    def test_view(self):
        logout()
        with self.assertRaises(ComponentLookupError):
            view = getMultiAdapter((self.document, self.request), name="timestamp")
        view = getMultiAdapter((self.file, self.request), name="timestamp")
        self.assertIn("This content is not timestamped.", view())
        self.assertFalse(view.is_timestamped())
        self.file.file = NamedBlobFile(data=b"file data", filename="file.txt")
        self.assertIn("This content is not timestamped.", view())
        self.assertFalse(view.is_timestamped())
        handler = ITimeStamper(self.file)
        handler.timestamp()
        self.assertIn("This content was timestamped on", view())
        self.assertEqual(
            view.more_infos_url(), "http://documentation.timestamptest.com"
        )
        self.assertTrue(view.is_timestamped())
        self.assertEqual(view.timestamp_date(), self.file.effective().asdatetime())
