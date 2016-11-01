# -*- coding: utf-8 -*-
"""
This modules provides networking functions on the ESP8266 board.
"""

import network

class Wlanclient:
    """Connect to a WiFi network

    Attributes:
        * cfg: Holds the configuration data
    """

    def __init__(self, cfg):

        #ap = network.WLAN(network.AP_IF)
        #ap.active(False)

        self.WLAN = None
        self.config = cfg

    def get_network(self):
        return self.WLAN

    def setup_network(self):
        self.WLAN = network.WLAN(network.STA_IF)
        self.WLAN.active(True)
        if not self.WLAN.isconnected():
            print('connecting to network...')
            self.WLAN.connect(self.config['ESSID'], self.config['PASSWORD'])
            while not self.WLAN.isconnected():
                pass
        print('network config: ', self.WLAN.ifconfig())
