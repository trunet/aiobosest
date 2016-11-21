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
from ..errors import (
    RESTConnectionError,
)

import logging


class PresetItem(object):
    """Defines a Preset

    Attributes:
        id: Preset ID
        source: :class:`.SourceItem`:
        type: Source location type
        location: uri or item number to locate the source
        sourceAccount: source account
        isPresetable: if this is preseatable or not
        itemName: Item name
    """
    def __init__(self):
        self.id = -1
        self.source = None
        self.type = None
        self.location = None
        self.sourceAccount = None
        self.isPresetable = False
        self.itemName = None


class Presets(BaseHelper):
    """Helper class for the /presets API method.

    Args:
        connection: Connection class
        is_updated: asyncio.Event() is set when an update happens

    Attributes:
        presets: :class:`.PresetItem`: list
    """
    def __init__(self, connection, is_updated=None):
        super().__init__(key_name='presets', is_updated=is_updated)

        self._connection = connection

        self.uri = '/presets'

        self.presets = list()
        self.sources = None

    async def parse(self, data):
        """Parse the XML into class properties.

        Args:
            data: string data to be parsed"""
        data = await super().xml_parse(data)
        if data is not None:
            self.presets = list()
            for item in data.xpath('./preset'):
                presetItem = PresetItem()
                presetItem.id = get_first_or_none(item.xpath('./@id'))[0]
                for source in self.sources.sources:
                    if source.source == get_first_or_none(item.xpath('./ContentItem/@source'))[0]:
                        presetItem.source = source
                presetItem.type = get_first_or_none(item.xpath('./ContentItem/@type'))[0]
                presetItem.location = get_first_or_none(item.xpath('./ContentItem/@location'))[0]
                presetItem.sourceAccount = get_first_or_none(item.xpath('./ContentItem/@sourceAccount'))[0]
                presetItem.isPresetable = get_first_or_none(item.xpath('./ContentItem/@isPresetable'))[0]
                presetItem.itemName = get_first_or_none(item.xpath('./ContentItem/itemName/text()'))[0]
                self.presets.append(presetItem)
            super().set_update()

    async def get(self):
        """Get /presets data using REST API."""
        data = await self._connection.get(self.uri)
        await self.parse(data)

    def set_sources(self, sources):
        self.sources = sources
