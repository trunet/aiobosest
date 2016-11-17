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

from aiobosest import BoseSoundTouch

import asyncio
import logging
import sys
import random
import socket
import time

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

logging.basicConfig(level=logging.DEBUG)

BOSE_ADDR = None


def on_service_state_change(zeroconf, service_type, name, state_change):
    global BOSE_ADDR
    logging.info("Service {} of type {} state changed: {}".format(
                 name, service_type, state_change))

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            BOSE_ADDR = '{}'.format(socket.inet_ntoa(info.address))


def main():
    global BOSE_ADDR

    loop = asyncio.get_event_loop()
    is_updated = asyncio.Event()

    zeroconf = Zeroconf()
    browser = ServiceBrowser(zeroconf, "_soundtouch._tcp.local.",
                             handlers=[on_service_state_change])

    start = time.time()
    while time.time() < start+3:
        if BOSE_ADDR:
            break
        logging.info("BoseSoundTouch System not found.")
        time.sleep(1)

    bosesoundtouch = BoseSoundTouch(BOSE_ADDR, is_updated)

    async def setVolume():
        await asyncio.sleep(3)
        await bosesoundtouch.volume.set(random.randint(0, 10))

    async def run():
        is_updated.clear()
        while True:
            await is_updated.wait()
            is_updated.clear()
            print('=' * 79)
            print("Volume: {}".format(bosesoundtouch.volume.actualvolume))
            print("Mute: {}".format(bosesoundtouch.volume.muteenabled))
            print("Source: {}".format(bosesoundtouch.nowplaying.source))
            print("Artist / Album / Track: {} / {} / {}".format(
                    bosesoundtouch.nowplaying.artist,
                    bosesoundtouch.nowplaying.album,
                    bosesoundtouch.nowplaying.track))

            percentage = int(
                    bosesoundtouch.nowplaying.time_elapsed /
                    bosesoundtouch.nowplaying.time_total * 70)
            sys.stdout.write("[%s]" % (" " * 70))
            sys.stdout.flush()
            sys.stdout.write("\b" * (70+1))
            for i in range(percentage):
                sys.stdout.write("-")
            sys.stdout.flush()
            sys.stdout.write("\n")
            print('=' * 79)

    try:
        volume_task = asyncio.ensure_future(setVolume())
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        if not volume_task.done():
            volume_task.cancel()
        logging.info('Caught keyboard interrupt, shutting down.')
        loop.run_until_complete(bosesoundtouch.shutdown())
    finally:
        logging.debug('Stopping loop.')
        loop.close()

if __name__ == '__main__':
    main()
