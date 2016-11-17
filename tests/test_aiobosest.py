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

import pytest

import asyncio
from lxml import etree

from aiobosest import BoseSoundTouch

BOSE_ADDR = '192.168.178.188'


@pytest.mark.asyncio
async def test_connect():
    """Test the connection with the system."""
    bosesoundtouch = BoseSoundTouch(BOSE_ADDR)
    await bosesoundtouch.is_running()

    assert True

    await bosesoundtouch.shutdown()


@pytest.mark.asyncio
async def test_receive_from_SoundTouch():
    """Test if you can GET from the REST API."""
    bosesoundtouch = BoseSoundTouch(BOSE_ADDR)
    await bosesoundtouch.is_running()

    info = await bosesoundtouch._connection.get('/info')
    assert 'SoundTouch' in etree.XML(info).xpath('/info/type/text()')[0]

    await bosesoundtouch.shutdown()


@pytest.mark.asyncio
async def test_get_now_playing():
    """/now_playing method test."""
    bosesoundtouch = BoseSoundTouch(BOSE_ADDR)
    await bosesoundtouch.is_running()

    assert bosesoundtouch.nowplaying.source is not None

    await bosesoundtouch.shutdown()


@pytest.mark.asyncio
async def test_get_volume():
    """/volume method test."""
    bosesoundtouch = BoseSoundTouch(BOSE_ADDR)
    await bosesoundtouch.is_running()

    assert bosesoundtouch.volume.actualvolume is not -1
    assert bosesoundtouch.volume.targetvolume is not -1
    assert bosesoundtouch.volume.muteenabled is not -1

    await bosesoundtouch.shutdown()


@pytest.mark.asyncio
async def test_key_press():
    """Button press test"""
    is_updated = asyncio.Event()
    bosesoundtouch = BoseSoundTouch(BOSE_ADDR, is_updated)
    await bosesoundtouch.is_running()

    previous_source = bosesoundtouch.nowplaying.source
    is_updated.clear()
    await bosesoundtouch.key.press('POWER')
    await is_updated.wait()
    actual_source = bosesoundtouch.nowplaying.source
    assert previous_source != actual_source

    bosesoundtouch.shutdown()
