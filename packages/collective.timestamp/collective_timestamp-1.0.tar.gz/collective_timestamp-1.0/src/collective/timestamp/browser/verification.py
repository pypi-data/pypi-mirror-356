# -*- coding: utf-8 -*-

from collective.timestamp.interfaces import ITimeStamper
from collective.timestamp.interfaces import ITimestampingSettings
from collective.timestamp.utils import get_timestamp_date_from_tsr_file
from plone import api
from Products.Five.browser import BrowserView


class VerificationView(BrowserView):

    def is_timestamped(self):
        handler = ITimeStamper(self.context)
        return handler.is_timestamped()

    def timestamp_date(self):
        tsr_file = self.context.timestamp
        timestamp_date = get_timestamp_date_from_tsr_file(tsr_file.data)
        return timestamp_date.astimezone()

    def more_infos_url(self):
        return api.portal.get_registry_record(
            "timestamping_documentation_url",
            interface=ITimestampingSettings,
        )
