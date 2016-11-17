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

__all__ = [
    'BoseSoundTouchError',
    'RESTConnectionError',
    'WSConnectionError',
    'RequestError',
    'CallError',
    'KeyNotFoundError',
]


class BoseSoundTouchError(Exception):
    """Base exception class for BoseSoundTouch exceptions."""


class RESTConnectionError(BoseSoundTouchError):
    """Raised if didn't connect to REST API Endpoint."""


class WSConnectionError(BoseSoundTouchError):
    """Raised if didn't connect to WebSocket."""


class RequestError(BoseSoundTouchError):
    """Raised if a request didn't receive HTTP 200."""


class CallError(BoseSoundTouchError):
    """Raised if a call produced errors or malformed requests."""


class KeyNotFoundError(BoseSoundTouchError):
    """Raised if a user try to set a key that doesn't exists."""
