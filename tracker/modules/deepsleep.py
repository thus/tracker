"""
Copyright (C) 2020 Mats Klepsland <mats.klepsland@gmail.com>.

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

import time
import socket
import logging
import tracker.globals

from pyroute2 import IPRoute


class TrackerDeepSleep:
    """Deepsleep tracker module.

    Used to track iphones and other devices that disconnects from the
    network when the screen is locked.

    """

    def defaults(self):
        """Apply module defaults."""
        return dict(
            interval=10,
            max_retries=10,
            retry_interval=2
        )

    def init(self):
        """Initialize module."""
        if "ip" not in self.config:
            logging.critical("'ip' must be specified when using deepsleep")
            return False

        return True

    def track(self):
        """Run device tracking."""
        for _ in range(self.config["max_retries"]):
            # Send packet on port UDP/5353
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)
            addr = (self.config["ip"], 5353)
            msg = b'All your base'
            try:
                s.sendto(msg, addr)
            except OSError as ex:
                logging.critical("Error sending packet: %s" % ex)
                return None

            # Check if device is present in ARP table
            with IPRoute() as ip:
                result = ip.get_neighbours(dst=self.config["ip"])
                if result and result[0]["state"] >= 2:
                    return True

            for i in range(self.config["retry_interval"]):
                if tracker.globals.terminate:
                    return None
                time.sleep(1)

        return False
