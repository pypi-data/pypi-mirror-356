# -*- coding: utf-8 -*-

from collective.timestamp.testing import COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING
from collective.timestamp.utils import timestamp
from collective.timestamp.utils import get_timestamp_date_from_tsr_file
from collective.timestamp.utils import localize_utc_date
from datetime import datetime, timedelta
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile

import unittest
import pytz


class TestUtils(unittest.TestCase):

    layer = COLLECTIVE_TIMESTAMP_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.my_file = api.content.create(
            container=self.portal,
            type="File",
            id="my-file",
        )
        self.my_file.file = NamedBlobFile(data=b"file data", filename="file.txt")
        self.file_data = self.my_file.file.data

    def test_localize_utc_date(self):
        naive_datetime = datetime(2024, 9, 10, 12, 0, 0)
        localized_datetime = localize_utc_date(naive_datetime)
        expected_datetime = datetime(2024, 9, 10, 12, 0, 0, tzinfo=pytz.UTC)
        self.assertEqual(localized_datetime, expected_datetime)

    def test_timestamp(self):
        tsr, timestamp_date = timestamp(self.file_data, "http://freetsa.org/tsr")
        self.assertIsInstance(tsr, bytes)
        self.assertIsInstance(timestamp_date, datetime)
        self.assertAlmostEqual(
            timestamp_date, datetime.now(pytz.UTC), delta=timedelta(seconds=10)
        )

    def test_timestamp_retries(self):
        tsr, timestamp_date = timestamp(
            self.file_data,
            "https://httpbin.org/status/429",
            use_failover=True,
            failover_timestamping_service_urls=[
                "https://httpbin.org/status/429",
                "http://freetsa.org/tsr",
            ],
            max_retries=2,
            initial_backoff_seconds=0.1,
        )
        self.assertIsInstance(tsr, bytes)
        self.assertIsInstance(timestamp_date, datetime)
        self.assertAlmostEqual(
            timestamp_date, datetime.now(pytz.UTC), delta=timedelta(seconds=10)
        )

    def test_timestamp_raises_connection_error(self):
        with self.assertRaises(ConnectionError):
            timestamp(
                self.file_data,
                "https://httpbin.org/status/500",
                use_failover=True,
                failover_timestamping_service_urls=["https://httpbin.org/status/429"],
                max_retries=2,
                initial_backoff_seconds=0.01,
            )

    def test_get_timestamp_date_from_tsr_file(self):
        tsr, timestamp_date = timestamp(self.file_data, "http://freetsa.org/tsr")
        verif_date = get_timestamp_date_from_tsr_file(tsr)
        self.assertEqual(timestamp_date, verif_date)
        self.assertAlmostEqual(
            verif_date, datetime.now(pytz.UTC), delta=timedelta(seconds=10)
        )
