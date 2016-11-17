# Copyright 2016 Wagner Sartori Junior
#
# This file is part of aiobosest.
#
# aiobosest is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# aiobosest is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with aiobosest.  If not, see <http://www.gnu.org/licenses/>.

from .base import *
from ..utils import get_first_or_none

import logging


class NowPlaying(BaseHelper):
    """Helper class for the /now_playing API method.

    Args:
        connection: Connection class
        is_updated: asyncio.Event() is set when an update happens

    Attributes:
        source: System source e.g. STANDBY or AUX
        itemName: Item name playing
        track: self explaining
        artist: self explaining
        album: self explaining
        art: URL of the art image
        artImageStatus: Image Status from ART_STATUS
        time_total: Total time when available
        time_elapsed: Elapsed time when available
        playStatus: Play status from PLAY_STATUS
        shuffleSetting: Is Shuffle ON
        repeatSetting: Is Repeat ON
        streamType: Stream Type
        trackID: Track ID
    """
    def __init__(self, connection, is_updated=None):
        super().__init__(key_name='nowPlaying', is_updated=is_updated)

        self._connection = connection

        self.uri = '/now_playing'

        self.source = None
        self.itemName = None
        self.track = None
        self.artist = None
        self.album = None
        self.art = None
        self.artImageStatus = None
        self.time_total = -1
        self.time_elapsed = -1
        self.playStatus = None
        self.shuffleSetting = None
        self.repeatSetting = None
        self.streamType = None
        self.trackID = None

    async def parse(self, data):
        """Parse the XML into class properties.

        Args:
            data: string data to be parsed"""
        data = await super().xml_parse(data)
        if data is not None:
            self.source = get_first_or_none(data.xpath('./ContentItem/@source'))[0]
            self.itemName = get_first_or_none(data.xpath('./ContentItem/itemName/text()'))[0]
            self.track = get_first_or_none(data.xpath('./track/text()'))[0]
            self.artist = get_first_or_none(data.xpath('./artist/text()'))[0]
            self.album = get_first_or_none(data.xpath('./album/text()'))[0]
            self.artImageStatus = get_first_or_none(data.xpath('./art/@artImageStatus'))[0]
            self.art = get_first_or_none(data.xpath('./art/text()'))[0]
            self.time_total = int(get_first_or_none(data.xpath('./time/@total'))[0] or -1)
            self.time_elapsed = int(get_first_or_none(data.xpath('./time/text()'))[0] or -1)
            self.playStatus = get_first_or_none(data.xpath('./playStatus/text()'))[0]
            self.shuffleSetting = get_first_or_none(data.xpath('./shuffleSetting/text()'))[0]
            self.repeatSetting = get_first_or_none(data.xpath('./repeatSetting/text()'))[0]
            self.streamType = get_first_or_none(data.xpath('./streamType/text()'))[0]
            self.trackID = get_first_or_none(data.xpath('./trackID/text()'))[0]

            super().set_update()

    async def get(self):
        """Get /now_playing data using REST API."""
        data = await self._connection.get(self.uri)
        await self.parse(data)
