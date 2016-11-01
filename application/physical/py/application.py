# -*- coding: utf-8 -*-
"""
The central class to tie all others together. Includes the main run() method.
"""

from utime import sleep_ms # pylint: disable=import-error
import ubinascii # pylint: disable=import-error
from ustruct import unpack # pylint: disable=import-error

class Application(object):
    """This is what runs in a "main loop" type of fashion.

    Todo:
        * make this a singleton
    """

    def __init__(self, components=None, config=None, network=None, mqttclient=None, fsm=None):

        self.fsm = fsm
        self.components = components
        self.config = config
        self.network = network
        self.mqttclient = mqttclient

    def run(self):
        while True:
            if self.fsm.current == 'INIT':
                self.fsm.readying()
            elif self.fsm.current == 'READY':
                self.components['button-1']['obj'].tick()
                self.components['button-2']['obj'].tick()
                self.mqttclient.check_msg()
                sleep_ms(20)
            elif self.fsm.current == 'ANIMATION':
                self.components['button-1']['obj'].tick()
                self.components['button-2']['obj'].tick()
                self.mqttclient.check_msg()
                self.components['WS2812_ledstrip_single-1']['obj'].update()
                sleep_ms(20)

    #pre/fix/$room/$deviceid/config
    #pre/fix/$room/$deviceid/commands
    #pre/fix/$room/$deviceid/components
    #pre/fix/$room/$deviceid/state
    #pre/fix/$room/$deviceid/events resetting|animating|readying
    def router(self, topic, msg):
        """This is called from the MQTTClient callback and stitches all modules together.
	"""

        #components
        if "{}/{}/components".format(self.config['MQTT']['TOPICBASE'], self.config['CLIENTID']) in topic:
            topiclist = topic.decode('utf-8').split('/')
            if   topiclist[-2] == "wakeuplight" and topiclist[-1] == "color1":
                self.components['WS2812_ledstrip_single-1']['obj'].color1 = unpack('BBB', ubinascii.unhexlify(msg.decode('utf-8').replace('#', '')))
            elif topiclist[-2] == "wakeuplight" and topiclist[-1] == "color2":
                self.components['WS2812_ledstrip_single-1']['obj'].color2 = unpack('BBB', ubinascii.unhexlify(msg.decode('utf-8').replace('#', '')))
            elif topiclist[-2] == "wakeuplight" and topiclist[-1] == "pattern_active":
                self.components['WS2812_ledstrip_single-1']['obj'].pattern_active = msg.decode('utf-8')
                if msg.decode('utf-8') == "NONE":
                    pass
                elif msg.decode('utf-8') == "BLINK":
                    self.components['WS2812_ledstrip_single-1']['obj'].setup_blink()
                elif msg.decode('utf-8') == "CA30":
                    self.components['WS2812_ledstrip_single-1']['obj'].setup_ca30()
                elif msg.decode('utf-8') == "CA90":
                    self.components['WS2812_ledstrip_single-1']['obj'].setup_ca90()
            elif topiclist[-2] == "wakeuplight" and topiclist[-1] == "interval":
                self.components['WS2812_ledstrip_single-1']['obj'].interval = int(msg.decode('utf-8'))

        #state
        elif "{}/{}/state".format(self.config['MQTT']['TOPICBASE'], self.config['CLIENTID']) in topic:
            topiclist = topic.decode('utf-8').split('/')

        #events
        elif "{}/{}/events".format(self.config['MQTT']['TOPICBASE'], self.config['CLIENTID']) in topic:
            topiclist = topic.decode('utf-8').split('/')
            if   topiclist[-1] == "events" and msg.decode('utf-8') == "readying":
                if self.fsm.can('readying'):
                    self.fsm.readying()
            elif topiclist[-1] == "events" and msg.decode('utf-8') == "animating":
                if self.fsm.can('animating'):
                    self.fsm.animating()
        else:
            pass
