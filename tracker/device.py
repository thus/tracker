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

import sys
import time
import logging
import multiprocessing
import globals
import paho.mqtt.client as mqtt

from modules import TrackerModule


def on_connect(client, userdata, flags, rc):
    """Call when the broker responds to our connection request.

    Args:
      client:   The client instance.
      userdata: The private user data set in client.
      flags:    Response flags sent by the broker.
      rc:       The connection result.

    """
    global loop_flag
    global conn_rc
    global conn_err

    conn_err = None
    conn_rc = rc

    if rc == 1:
        conn_err = "Connection refused - incorrect protocol version"
    elif rc == 2:
        conn_err = "Connection refused - invalid client identifier"
    elif rc == 3:
        conn_err = "Connection refused - server unavailable"
    elif rc == 4:
        conn_err = "Connection refused - bad username or password"
    elif rc == 5:
        conn_err = "Connection refused - not authorized"
    elif rc > 5:
        conn_err = "Connection refused - unused error code"

    loop_flag = 0


def connect_mqtt(name, config):
    """Connect to MQTT broker.

    Args:
      name (str):    Name of the device.
      config (dict): Application config.

    Returns:
      MQTT client.

    """
    global loop_flag
    loop_flag = 1

    client = mqtt.Client("tracker-%s" % name)
    client.on_connect = on_connect

    if "username" in config["mqtt"] and "password" in config["mqtt"]:
        client.username_pw_set(username=config["mqtt"]["username"],
                               password=config["mqtt"]["password"])

    try:
        client.connect(config["mqtt"]["broker"], port=config["mqtt"]["port"])
    except ConnectionRefusedError as ex:
        globals.terminate = True
        logging.critical("Could not connect to MQTT: %s" % ex)
        sys.exit(1)

    client.loop_start()

    while loop_flag == 1:
        time.sleep(.01)

    if conn_err:
        globals.terminate = True
        logging.critical("Could not connect to MQTT: [Errno %d] %s" %
                         (conn_rc, conn_err))
        sys.exit(1)

    return client


def device_track(name, device, config):
    """Run tracker process.

    Args:
      name (str):    Name of the device.
      device (dict): Device config.
      config (dict): Application config.

    """
    m = TrackerModule(module=device["module"], device=device, config=config)

    if m.init() is False:
        logging.critical("Error initializing '%s'. Terminating." % name)
        globals.terminate = True
        return

    last_state = None

    while not globals.terminate:
        home = m.track()
        if home:
            state = config["state"]["home"]
        elif home is None:
            break
        else:
            state = config["state"]["not_home"]

        logging.debug("Module returned '%s' for device '%s'" % (state, name))

        if state != last_state:
            logging.info("Device '%s' changed state to %s" % (name, state))
            client = connect_mqtt(name, config)
            client.publish("%s%s" % (config["mqtt"]["topic_prefix"],
                           name), state)
            client.disconnect()
            client.loop_stop()
            last_state = state

        for i in range(m.module.config["interval"]):
            if globals.terminate:
                break
            time.sleep(1)

    m.deinit()


def devices_start_tracking(config):
    """Start tracking devices.

    Create a process per device that should be tracked.

    Args:
      config (dict): application configuration.

    Returns:
      List of processes.

    """
    devices = list()

    for item in config["device_track"]:
        for name, device in item.items():
            logging.debug("Tracking device '%s'" % name)
            p = multiprocessing.Process(target=device_track,
                                        args=(name, device, config,))
            p.start()
            devices.append(p)

    return devices
