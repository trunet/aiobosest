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

from .log import logger
from .errors import (
    RESTConnectionError,
    WSConnectionError,
    RequestError,
    CallError,
)

import asyncio
import logging

import aiohttp
from lxml import etree

__all__ = [
    'Connection',
]

HTTP_REST_TIMEOUT = 5


class Connection:
    """Connection class to connect on the system.

    Also provides REST methods to get or post.

    Args:
        address: Bose SoundTouch IP address
        loop: asyncio loop if you want to provide one

    Attributes:
        websocket: websocket connection"""
    def __init__(self, address, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()

        self._address = address
        self._loop = loop

        self._session = aiohttp.ClientSession()

        self.websocket = None

    async def connect_websocket(self):
        """Connect to the websocket."""
        self.websocket = await self._session.ws_connect(
            'http://{address}:8080'.format(address=self._address),
            protocols=['gabbo'])

    async def shutdown(self):
        """Needs to be called before application quit. This is called by main the class"""
        if self.websocket:
            await self.websocket.close()
        await self._session.close()

    async def _status_xml_parse(self, data):
        """Parse the XML status message.

        Args:
            data: string data to be parsed

        Returns:
            True if status, False if error"""
        xmltree = etree.XML(data)
        errors = xmltree.xpath('/errors')
        if errors:
            logging.error('XML Error: {errors}'.format(errors=errors))
            return False
        status = xmltree.xpath('/status/text()')
        if status:
            logging.debug('XML Status: {status}'.format(status=status))
        return True

    async def get(self, uri):
        """GET data using the REST API

        Args:
            uri: URI to get the data

        Returns:
            XML data string

        Raises:
            CallError: malformed requests
            RequestError: request didn't receive HTTP 200
            RestConnectionError: other errors"""
        logging.debug('>>> REST URI: http://{address}:8090{uri}'.format(
                        address=self._address, uri=uri))
        try:
            with aiohttp.Timeout(HTTP_REST_TIMEOUT, loop=self._loop):
                async with self._session.get('http://{address}:8090{uri}'.format(
                                            address=self._address, uri=uri)) as resp:
                    data = await resp.read()
                    logging.debug('<<< RECEIVED FROM URI http://{address}:8090{uri}: {message}'
                                  .format(address=self._address, uri=uri, message=data))
                    status = await self._status_xml_parse(data)
                    if status:
                        return data
                    else:
                        raise CallError
        except CallError:
            raise
        except RequestError:
            raise
        except Exception as e:
            logging.error('Error connecting to http://{address}:8090: {error!r}'.format(
                          address=self._address, error=e))
            raise RESTConnectionError(e)

    async def post(self, uri, message):
        """POST data using the REST API

        Args:
            uri: URI to get the data
            message: XML message to POST

        Returns:
            XML data string

        Raises:
            CallError: malformed requests
            RequestError: request didn't receive HTTP 200
            RestConnectionError: other errors"""
        logging.debug('>>> POST {message} ON URI http://{address}:8090{uri}'.format(
                      address=self._address, uri=uri, message=message))
        try:
            with aiohttp.Timeout(HTTP_REST_TIMEOUT, loop=self._loop):
                async with self._session.post('http://{address}:8090{uri}'.format(
                        address=self._address, uri=uri, data=message), data=message) as resp:
                    if resp.status != 200:
                        raise RequestError
                    data = await resp.read()
                    logging.debug('<<< RECEIVED FROM URI http://{address}:8090{uri}: {message}'
                                  .format(address=self._address, uri=uri, message=data))
                    status = await self._status_xml_parse(data)
                    if status:
                        return data
                    else:
                        raise CallError
        except CallError:
            raise
        except RequestError:
            raise
        except Exception as e:
            logging.error('Error connecting to http://{address}:8090: {error!r}'.format(
                          address=self._address, error=e))
            raise RESTConnectionError(e)
