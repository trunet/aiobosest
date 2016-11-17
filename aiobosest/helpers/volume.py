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


class Volume(BaseHelper):
    """Helper class for the /volume API method.

    Args:
        connection: Connection class
        is_updated: asyncio.Event() is set when an update happens

    Attributes:
        targetvolume: Target volume when setting
        actualvolume: Actual volume
        muteenabled: Is mute enabled?
    """
    def __init__(self, connection, is_updated=None):
        super().__init__(key_name='volume', is_updated=is_updated)

        self._connection = connection

        self.uri = '/volume'

        self.targetvolume = -1
        self.actualvolume = -1
        self.muteenabled = False

    async def parse(self, data):
        """Parse the XML into class properties.

        Args:
            data: string data to be parsed"""
        data = await super().xml_parse(data)
        if data is not None:
            self.targetvolume = int(
                    get_first_or_none(data.xpath('./targetvolume/text()'))[0] or -1)
            self.actualvolume = int(
                    get_first_or_none(data.xpath('./actualvolume/text()'))[0] or -1)
            self.muteenabled = True if get_first_or_none(
                    data.xpath('./muteenabled/text()'))[0] == 'true' else False

            super().set_update()

    async def get(self):
        """Get /volume data using REST API."""
        data = await self._connection.get(self.uri)
        await self.parse(data)

    async def set(self, volume):
        """Set the volume.

        Args:
            volume: Volume to set"""
        msg = '<volume>{volume}</volume>'.format(volume=volume)
        logging.info('Setting volume to {volume}'.format(volume=volume))
        try:
            await self._connection.post(self.uri, msg)
        except RESTConnectionError:
            pass
