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

import sys
import yaml

DEFAULT_STATE_HOME = "home"
DEFAULT_STATE_NOT_HOME = "not_home"
DEFAULT_MQTT_BROKER = "localhost"
DEFAULT_MQTT_PORT = "1833"
DEFAULT_MQTT_TOPIC_PREFIX = "tracker/location/"


def _dict_nested_set(d, keys, value):
    """Set a nested key in a dictionary.

    Args:
      d (dict):    The dictionary.
      keys (list): The nested key.
      value:       The value to set the key to.

    """
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value


def _dict_nested_isset(d, keys):
    """Check if nested key is set in dictionary.

    Args:
      d (dict):    The dictionary.
      keys (list): The nested key.

    Returns:
      True if key is set, False otherwise.

    """
    _d = d

    for key in keys:
        try:
            _d = _d[key]
        except KeyError:
            return False

    return True


def config_apply_defaults(conf):
    """Apply defaults to the config where key is not set.

    Args:
      conf (dict): The loaded config.

    Returns:
      Dictionary containing config, with added defaults.

    """

    if not _dict_nested_isset(conf, ["state", "home"]):
        _dict_nested_set(conf, ["state", "home"], DEFAULT_STATE_HOME)

    if not _dict_nested_isset(conf, ["state", "not_home"]):
        _dict_nested_set(conf, ["state", "not_home"], DEFAULT_STATE_NOT_HOME)

    if not _dict_nested_isset(conf, ["mqtt", "broker"]):
        _dict_nested_set(conf, ["mqtt", "broker"], DEFAULT_MQTT_BROKER)

    if not _dict_nested_isset(conf, ["mqtt", "port"]):
        _dict_nested_set(conf, ["mqtt", "port"], DEFAULT_MQTT_PORT)

    if not _dict_nested_isset(conf, ["mqtt", "topic_prefix"]):
        _dict_nested_set(conf, ["mqtt", "topic_prefix"],
                         DEFAULT_MQTT_TOPIC_PREFIX)

    return conf


def config_load(config_file):
    """Load configuration file (YAML).

    Args:
      config_file (str): Configuration file.

    Returns:
      Dictionary containing config.

    """
    try:
        with open(config_file, "r") as f:
            conf = yaml.safe_load(f)
    except yaml.YAMLError as ex:
        sys.exit("ERROR: could not parse config file '%s': %s" %
                 (config_file, ex))
    except FileNotFoundError:
        sys.exit("ERROR: could not find config file '%s'" % config_file)

    config_apply_defaults(conf)

    if "device_track" not in conf:
        sys.exit("Config does not contain any devices to track. Exiting.")

    return conf
