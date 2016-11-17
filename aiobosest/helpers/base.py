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

import asyncio
import logging

from lxml import etree

ART_STATUS = [
    'INVALID',
    'SHOW_DEFAULT_IMAGE',
    'DOWNLOADING',
    'IMAGE_PRESENT',
]

KEY_VALUE = [
    'PLAY',
    'PAUSE',
    'STOP',
    'PREV_TRACK',
    'NEXT_TRACK',
    'THUMBS_UP',
    'THUMBS_DOWN',
    'BOOKMARK',
    'POWER',
    'MUTE',
    'VOLUME_UP',
    'VOLUME_DOWN',
    'PRESET_1',
    'PRESET_2',
    'PRESET_3',
    'PRESET_4',
    'PRESET_5',
    'PRESET_6',
    'AUX_INPUT',
    'SHUFFLE_OFF',
    'SHUFFLE_ON',
    'REPEAT_OFF',
    'REPEAT_ONE',
    'REPEAT_ALL',
    'PLAY_PAUSE',
    'ADD_FAVORITE',
    'REMOVE_FAVORITE',
    'INVALID_KEY',
]

KEY_STATE = [
    'press',
    'release',
]

PLAY_STATUS = [
    'PLAY_STATE',
    'PAUSE_STATE',
    'STOP_STATE',
    'BUFFERING_STATE',
    'INVALID_PLAY_STATUS',
]

SOURCE_STATUS = [
    'UNAVAILABLE',
    'READY',
]


class BaseHelper:
    """BaseHelper class for all the API methods available on Bose SoundTouch.

    Args:
        key_name: The XML Element name. e.g. 'volume'
        is_updated: asyncio.Event() is set when an update happens
    """

    def __init__(self, key_name=None, is_updated=None):
        if is_updated is None:
            is_updated = asyncio.Event()

        self.key_name = key_name
        self.is_updated = is_updated

    async def xml_parse(self, data):
        """Parse the XML data taking into consideration if it's coming from WebSocket or not.

        Args:
            data: string data to be parsed

        Returns:
            An XMLElement relative to the key_name"""
        xmldata = etree.XML(data)
        updates = xmldata.xpath('/updates')
        if updates:
            updated = updates[0].xpath('./{key_name}Updated/{key_name}'.format(
                                        key_name=self.key_name))
            if updated:
                return updated[0]
        if xmldata.xpath('/{key_name}'.format(key_name=self.key_name)):
            return xmldata

    def set_update(self):
        """Set the is_updated event"""
        self.is_updated.set()

    async def get(self):
        """Stub for get method"""
        pass

    async def set(self):
        """Stub for set method"""
        pass
