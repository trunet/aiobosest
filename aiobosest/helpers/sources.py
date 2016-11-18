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


class SourceItem(object):
    """Defines a SourceItem

    Attributes:
        source: Source
        sourceAccount: Account used on the source
        status: Source status
        isLocal: If is local on the system
        name: Name or account used on the source
    """
    def __init__(self):
        self.source = None
        self.sourceAccount = None
        self.status = None
        self.isLocal = False
        self.name = None


class Sources(BaseHelper):
    """Helper class for the /sources API method.

    Args:
        connection: Connection class
        is_updated: asyncio.Event() is set when an update happens

    Attributes:
        sources = :class:`SourceItem` list
    """
    def __init__(self, connection, is_updated=None):
        super().__init__(key_name='sources', is_updated=is_updated)

        self._connection = connection

        self.uri = '/sources'

        self.sources = list()

    async def parse(self, data):
        """Parse the XML into class properties.

        Args:
            data: string data to be parsed"""
        data = await super().xml_parse(data)
        if data is not None:
            self.sources = list()
            for item in data.xpath('./sourceItem'):
                sourceItem = SourceItem()
                sourceItem.source = get_first_or_none(item.xpath('./@source'))[0]
                sourceItem.sourceAccount = get_first_or_none(item.xpath('./@sourceAccount'))[0]
                sourceItem.status = get_first_or_none(item.xpath('./@status'))[0]
                sourceItem.isLocal = True if get_first_or_none(
                        item.xpath('./@isLocal'))[0] == 'true' else False
                sourceItem.name = get_first_or_none(item.xpath('./text()'))[0]
                self.sources.append(sourceItem)
            super().set_update()

    async def get(self):
        """Get /sources data using REST API."""
        data = await self._connection.get(self.uri)
        await self.parse(data)
