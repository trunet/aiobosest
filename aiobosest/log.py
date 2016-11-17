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

import logging

try:
    NullHandler = logging.NullHandler
except AttributeError:
    # Python 2.6 fallback
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logger = logging.getLogger(__package__)
logger.addHandler(NullHandler())

if logger.level == logging.NOTSET:
    logger.setLevel(logging.WARN)
