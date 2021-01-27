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

import argparse

DEFAULT_CONFIG_FILE = "/etc/tracker.yaml"


def read_args():
    """Read command-line arguments.

    Returns:
      Parsed arguments.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-file",
                        default=DEFAULT_CONFIG_FILE, metavar="FILE")
    args = parser.parse_args()

    return args
