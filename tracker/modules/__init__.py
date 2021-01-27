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

from .deepsleep import TrackerDeepSleep

MODULE_DEFAULT_INTERVAL = 60

# Add new modules here
MODULES = {
    "deepsleep": TrackerDeepSleep()
}


class TrackerModule:
    def __init__(self, *, module: str, device: dict, config: dict):
        if module in MODULES:
            self.module = MODULES[module]
        else:
            raise ValueError("Unknown module '%s'" % module)

        try:
            self.module.config = self.module.defaults()
        except AttributeError:
            self.module.config = dict()

        try:
            self.module.config.update(config["module"][module])
        except KeyError:
            pass

        self.module.config.update(device)

        if "interval" not in self.module.config:
            self.module.config["interval"] = MODULE_DEFAULT_INTERVAL

    def init(self):
        """Initializes the tracker module.

        Returns:
          True on success, False otherwise.

        """
        try:
            status = self.module.init()
        except AttributeError:
            status = True
        return status

    def track(self):
        """Runs the tracker module.

        Returns:
          True if device is present, False otherwise.

        """
        return self.module.track()

    def deinit(self):
        """Deinitializes the tracker module.

        Returns:
          True on success, False otherwise.

        """
        try:
            status = self.module.deinit()
        except AttributeError:
            status = True
        return status
