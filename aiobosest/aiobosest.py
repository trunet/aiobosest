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

from .helpers import (
    Key,
    NowPlaying,
    Volume,
)
from .log import logger
from .connection import (
    Connection,
)
from .errors import (
    RESTConnectionError,
)

import asyncio
import logging

import aiohttp

__all__ = [
    'BoseSoundTouch',
]


class BoseSoundTouch:
    """Main Bose SoundTouch Class.

    Args:
        address: Bose SoundTouch IP address
        is_updated: asyncio.Event() is set when an update happens
        loop: asyncio loop if you want to provide one

    Attributes:
        key: :class:`.Key` Class
        nowplaying: :class:`.NowPlaying` Class
        volume: :class:`.Volume` Class
    """
    def __init__(self, address, is_updated=None, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        if is_updated is None:
            is_updated = asyncio.Event()

        self._connection = Connection(address, loop)
        self._loop = loop
        self.is_updated = is_updated

        self._running = False

        self.key = Key(connection=self._connection, is_updated=self.is_updated)
        self.nowplaying = NowPlaying(connection=self._connection, is_updated=self.is_updated)
        self.volume = Volume(connection=self._connection, is_updated=self.is_updated)

        self._reader_task = asyncio.ensure_future(self._read_data(), loop=self._loop)

    async def shutdown(self):
        """Needs to be called before application quit."""
        await self._connection.shutdown()
        if not self._reader_task.done():
            self._reader_task.cancel()

    async def is_running(self):
        """Wait for reader task running.

        Returns:
            True when reader task is running"""
        while not self._running:
            await asyncio.sleep(.1)
        return True

    async def _read_data(self):
        """Always running reader task on the websocket port."""
        try:
            await self.key.get()
            await self.nowplaying.get()
            await self.volume.get()
        except RESTConnectionError as e:
            logging.critical('Error connecting to your BoseSoundTouch system, '
                             'read loop from websocket will not run')
            return

        logging.info('Connecting to the BoseSoundTouch WebSocket...')
        await self._connection.connect_websocket()
        while True:
            self._running = True
            try:
                msg = await self._connection.websocket.receive()
            except asyncio.CancelledError as e:
                logging.info('Closing WebSocket.')
                self._running = False
                break
            except Exception as e:
                logging.critical('Exception receiving from websocket: {!r}'.format(e))
                self._running = False
                break
            logging.debug('<<< WEBSOCKET: {}'.format(msg))
            if msg.type == aiohttp.WSMsgType.TEXT:
                await self.key.parse(msg.data)
                await self.nowplaying.parse(msg.data)
                await self.volume.parse(msg.data)
