# -*- coding: utf-8 -*-
"""
This modules provides code to connect to a MQTT broker.

Todo:
    * Check if a reconnect is necessary
    * Check if a connection already exists
"""

from umqtt.simple import MQTTClient # pylint: disable=import-error

class Client:
    """Connects with a supplied client id to the configured MQTT message broker.

    Tested with mosquitto version 1.4.10.

    Attributes:
        clientid (str): How this client identifies to the broker.
	    With mosquitto this is NOT the username.
	cfg (dict of str): The mandatory configuration object
    """

    def __init__(self, clientid, cfg,
                 callback=None,
                 app=None,
                 components=None,
                 config=None,
                 network=None):

        self.fsm = None
        self.app = app
        self.components = components
        self.config = config
        self.network = network

        self.mqttclient = None
        self.config = cfg
        self.CLIENTID = clientid
        self.CLIENTID = str(self.CLIENTID)
        self.callback = None

        if callback is not None:
            print('callback override!')
            self.callback = callback
        else:
            self.callback = self.subscribe_callback

        print(self.config)
        #print(self.CLIENTID)

    def get_mqttclient(self):
        """Return its own instance.
	"""
        return self.mqttclient

    def setup_mqttclient(self):
        """A wrapper around the umqtt.simple.py reference implementation
	"""
        self.mqttclient = MQTTClient("foobar", self.config['SERVER'])
        self.mqttclient.set_callback(self.callback)
        self.mqttclient.connect()
        self.mqttclient.subscribe("{}/{}/commands/#".format(self.config['TOPICBASE'], self.CLIENTID))
        self.mqttclient.subscribe("{}/{}/components/#".format(self.config['TOPICBASE'], self.CLIENTID))
        self.mqttclient.subscribe("{}/{}/config/#".format(self.config['TOPICBASE'], self.CLIENTID))
        self.mqttclient.subscribe("{}/{}/state/#".format(self.config['TOPICBASE'], self.CLIENTID))
        self.mqttclient.subscribe("{}/{}/events/#".format(self.config['TOPICBASE'], self.CLIENTID))
        self.mqttclient.publish('local/homeautomation/test', '+++' + self.config['TOPIC_PREFIX'])
        self.mqttclient.subscribe(self.config['TOPIC_PREFIX'] + '/config/+')

    def subscribe_callback(self, topic, msg):
        """Called when a message on a subscribed topic is received.
        """
        #print("Original callback {} {}".format(topic, msg))
        try:
            self.app.router(topic, msg)
        except:
            print("subscribe_callback could not call self.app.router(topic, msg)")
