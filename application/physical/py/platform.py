# -*- coding: utf-8 -*-
"""
Reads configuration files in json format.

Todo:
    * Split up into parts
"""

import ubinascii # pylint: disable=import-error
import machine # pylint: disable=import-error
import ujson # pylint: disable=import-error

class Config:
    """Holds configuration data for application-wide access.
    """

    def __init__(self):

        self.config = {
            "CLIENTID": b"ESP8266_" + ubinascii.hexlify(machine.unique_id()),
            "MQTT": {
                "SERVER": b"broker.christianprior.de",
                "TOPICBASE": b"bar"
            }
        }
        self.load_config()

    def load_config(self):
        try:
            with open("/config.json") as file:
                config = ujson.loads(file.read())
        except (OSError, ValueError):
            print("Couldn't load /config.json")
            #todo save defaults?
        else:
            self.config.update(config)
            print("Loaded config from /config.json")

        self.config['CLIENTID'] = self.config['CLIENTID'].decode('utf-8')
        self.config['MQTT']['TOPICBASE'] = b"{}/{}".format(self.config['MQTT']['TOPIC_PREFIX'], self.config['MQTT']['TOPIC'])

    def get_config(self):
        return self.config


class Components:
    """Holds component descriptions to attached physical parts.
    """

    def __init__(self):

        self.COMPONENTS = {
            "led-internal": {
                "logicalname": "led-internal",
                "pin": "2"
            }
        }

        self.load_components()

    def load_components(self):
        try:
            with open("/components.json") as file:
                components = ujson.loads(file.read())
        except (OSError, ValueError):
            print("Couldn't load /components.json")
            self.COMPONENTS['ERROR'] = b'Failed ujson.loads() of /components.json'
            #todo save defaults?
        else:
            self.COMPONENTS.update(components)
            print("Loaded config from /components.json")

    def get_components(self):
        return self.COMPONENTS

    def setup_components(self):
        for key in self.get_components():
            if key == 'led-internal':
                from machine import Pin # pylint: disable=import-error
                self.COMPONENTS[key]['obj'] = Pin(int(self.COMPONENTS[key]['pin']), Pin.OUT, value=1)
            elif key == 'button-1':
                from OneButton import OneButton # pylint: disable=import-error
                if self.COMPONENTS[key]['driver'] == 'OneButton':
                    self.COMPONENTS[key]['obj'] = OneButton(int(self.COMPONENTS[key]['pin']), self._str_to_bool(self.COMPONENTS[key]['activeLow']))
                    self.COMPONENTS[key]['obj'].name = self.COMPONENTS[key]['logicalname']
                    self.COMPONENTS[key]['obj'].attachClick(self.click)
                    self.COMPONENTS[key]['obj'].attachDoubleClick(self.doubleclick)
                    self.COMPONENTS[key]['obj'].attachLongPressStart(self.startLong)
                    self.COMPONENTS[key]['obj'].attachDuringLongPress(self.duringLong)
                    self.COMPONENTS[key]['obj'].attachLongPressStop(self.stopLong)
                else:
                    pass
            elif key == 'button-2':
                from OneButton import OneButton # pylint: disable=import-error
                if self.COMPONENTS[key]['driver'] == 'OneButton':
                    self.COMPONENTS[key]['obj'] = OneButton(int(self.COMPONENTS[key]['pin']), self._str_to_bool(self.COMPONENTS[key]['activeLow']))
                    self.COMPONENTS[key]['obj'].name = self.COMPONENTS[key]['logicalname']
                    self.COMPONENTS[key]['obj'].attachClick(self.click)
                    self.COMPONENTS[key]['obj'].attachDoubleClick(self.doubleclick)
                    self.COMPONENTS[key]['obj'].attachLongPressStart(self.startLong)
                    self.COMPONENTS[key]['obj'].attachDuringLongPress(self.duringLong)
                    self.COMPONENTS[key]['obj'].attachLongPressStop(self.stopLong)
                else:
                    pass
            elif key == 'WS2812_ledstrip_single-1':
                if self.COMPONENTS[key]['driver'] == 'NeoPixel':
                    from machine import Pin # pylint: disable=import-error
                    from neopixel import NeoPixel # pylint: disable=import-error
                    pin = Pin(int(self.COMPONENTS[key]['pin']), Pin.OUT)
                    self.COMPONENTS[key]['obj'] = NeoPixel(pin, int(self.COMPONENTS[key]['ledcount']))
                    for i in range(int(self.COMPONENTS[key]['ledcount'])):
                        self.COMPONENTS[key]['obj'][i] = (0, 0, 0)
                    self.COMPONENTS[key]['obj'].write()
                elif self.COMPONENTS[key]['driver'] == 'Ledstrip':
                    from plarin.ledstrip import Ledstrip # pylint: disable=import-error
                    self.COMPONENTS[key]['obj'] = Ledstrip(int(self.COMPONENTS[key]['pin']), int(self.COMPONENTS[key]['ledcount']))
                else:
                    pass
            else:
                pass
                #print(key)

    #Helper
    def _str_to_bool(self, string):
        #http://stackoverflow.com/a/21732183
        if string == 'True':
            return True
        elif string == 'False':
            return False
        else:
            raise ValueError("Cannot convert {} to a bool".format(string))

    #button
    def click(self, pin, msg=""):
        print('Pin {} click and msg {}'.format(pin.name, str(msg)))

    def doubleclick(self, pin, msg=""):
        print('Pin %s doubleclick and msg %s' % (pin.name, str(msg)))

    def startLong(self, pin, msg=""):
        print('Pin %s startLong and msg %s' % (pin.name, str(msg)))

    def duringLong(self, pin, msg=""):
        print('Pin %s duringLong and msg %s' % (pin.name, str(msg)))

    def stopLong(self, pin, msg=""):
        print('Pin %s stopLong and msg %s' % (pin.name, str(msg)))

