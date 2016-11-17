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
    KeyNotFoundError,
)

import logging


class Key(BaseHelper):
    """Helper class for the /key API method.

    Args:
        connection: Connection class
        is_updated: asyncio.Event() is set when an update happens

    Attributes:
        state: Button state, should match KEY_STATE
        value: Button value, should match KEY_VALUE
    """
    def __init__(self, connection, is_updated=None):
        super().__init__(key_name='key', is_updated=is_updated)

        self._connection = connection

        self.uri = '/key'

        self.state = None
        self.value = None

    async def parse(self, data):
        """Parse the XML into class properties.

        Args:
            data: string data to be parsed"""
        data = await super().xml_parse(data)
        if data is not None:
            self.state = get_first_or_none(data.xpath('./@state'))[0] or None
            self.value = get_first_or_none(data.xpath('./text()'))[0] or None

            super().set_update()

    async def press(self, button):
        """Implements buttons being pressed and released.

        Args:
            button: Button to be pressed, should match KEY_VALUE

        Raises:
            KeyNotFound: When button is not defined in KEY_VALUE"""
        if button not in KEY_VALUE:
            raise KeyNotFound
        for state in KEY_STATE:
            msg = '<key state="{state}" sender="Gabbo">{value}</key>'.format(
                    value=button, state=state)
            logging.info('Sending key {value} with state {state}'.format(
                    value=button, state=state))
            try:
                await self._connection.post(self.uri, msg)
            except RESTConnectionError:
                pass
