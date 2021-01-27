"""
Copyright (C) 2020 Mats Klepsland <mats.klepsland@gmail.com>

This file is part of Tracker.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

import logging.config
import signal
import globals

from args import read_args
from config import config_load
from device import devices_start_tracking


def signal_handler(signum, frame):
    globals.terminate = True


def main():
    globals.initialize()

    signal.signal(signal.SIGINT, signal_handler)

    args = read_args()
    config = config_load(args.config_file)

    if "logging" in config:
        logging.config.dictConfig(config["logging"])

    logging.info("Starting tracker")

    devices = devices_start_tracking(config)

    for device in devices:
        device.join()

    logging.info("Stopping tracker")


if __name__ == "__main__":
    main()
