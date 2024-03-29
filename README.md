# Tracker

Device tracking for home automation (e.g home assistant), running as an external
service, and reporting status to a MQTT broker.

Tracking is configured per device, using a set of pre-defined modules. As of
now, only the *deepsleep* module is implemented.

![Image of Tracker from Paw Patrol](images/tracker.png)

*(Image source: https://pawpatrol.fandom.com/wiki/Tracker)*

## Modules

### Deepsleep

This module works by sending a UDP packet on port 5353 (used by multicast DNS)
with whatever payload to a device, and then checking the host machines ARP table
to see if it contains an entry for the device we are tracking.

This module enables us to track newer iPhones, which are hard to track, since
they disconnect from WiFi when the screen is locked. This method probably works
for other devices as well.

This module basically uses the same detection strategy as implemented by Magnus
Nyström (mudape) in [iphonedetect](https://github.com/mudape/iphonedetect).
I had to do my own implementation, since I wanted to track devices on an other
subnet than the Home Assistant server, which would not work with iphonedetect,
since the server was not getting ARP table entries for the devices.

## Installation

Tracker can be installed in the following way.

Start by installing the Tracker Python module:
```bash
root@server:~/tracker# pip3 install -r requirements.txt
root@server:~/tracker# python3 setup.py install
```

Then add a configuration file for Tracker. The simplest way to do this is to
copy the example configuration file from the repository and edit it to fit your
needs:
```bash
root@server:~/tracker# mkdir /etc/tracker
root@server:~/tracker# cp example.yaml /etc/tracker/tracker.yaml
```

And then finally, install the Tracker systemd service:
```bash
root@server:~/tracker# cp tracker.service /etc/systemd/system
root@server:~/tracker# systemctl daemon-reload
root@server:~/tracker# systemctl enable tracker.service
root@server:~/tracker# systemctl start tracker.service
```
Above, we also tell systemd to start Tracker on boot.

## Use together with Home Assistant

### Install Mosquitto broker
In this example, we use the Mosquitto MQTT broker from the Home Assistant add-on
store. Feel free to use any MQTT broker you like.

Start by installing the Mosquitto broker from the add-on store and add a local
user to the configuration file (Supervisor → Mosquitto broker → Configuration),
e.g:

```yaml
logins:
  - username: tracker
    password: some-awesome-random-generated-password
```

The broker needs to be restarted before we are able to log in with the new user.

### Add device_tracker config to configuration.yaml

To actually track the device, we have to add some configuration to
/config/configuration.yaml (or maybe in another location if HASSOS is not used).
This can be done using SSH or using the *File Editor* add-on.

The following configuration tracks the device *my_iphone* using the
*tracker/location/my_iphone* MQTT topic:

```yaml
device_tracker:
  - platform: mqtt
    devices:
      my_iphone: tracker/location/my_iphone
```

Home Assistant should be restarted after modifying *configuration.yaml*.

This means that every time Tracker publishes something on that MQTT topic, it is
picked up by Home Assistant.

### Configure Tracker

The following should be added to the configuration file of Tracker (default
path: */etc/tracker.yaml*) to track the device configured in the previous step:

```yaml
device_track:
  - my_iphone:
    module: deepsleep
    ip: 1.2.3.4  # add the IP address of your device here
```

Now start Tracker to start tracking your device.
