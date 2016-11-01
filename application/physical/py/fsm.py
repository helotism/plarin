# -*- coding: utf-8 -*-
"""
A wrapper around the Python port of the popular JavaScript state machine by Jake Gordon.

See https://github.com/jakesgordon/javascript-state-machine for the original,
and https://github.com/foobarto/fysom for the port.
"""

from foobartofysomstripped import Fysom # pylint: disable=import-error

class FiniteStateMachine(object):
    """Subclassing Fysom with the necessary adaptations.

    Attributes:
        mqttclient: The object to send log-like status changes through.
    """

    def __init__(self, components=None, config=None, network=None, mqttclient=None):

        self.fsm = None
        self.components = components
        self.config = config
        self.network = network
        self.mqttclient = mqttclient

    def get_finitestatemachine(self):
        return self.fsm

    def setup_finitestatemachine(self):

        self.fsm = Fysom({

            'initial': {'state': 'INIT', 'event': 'initializing'},

            'events': [
                {'name': 'readying', 'src': ['INIT', 'ANIMATION'], 'dst': 'READY'},
                {'name': 'erring', 'src': ['INIT', 'READY'], 'dst': 'ERROR'},
                {'name': 'resetting', 'src': ['READY', 'ERROR'], 'dst': 'INIT'},
                {'name': 'animating', 'src': 'READY', 'dst': 'ANIMATION'}
            ],

            'callbacks': {
                'onbeforeinitializing': self.onbeforeinitializing,
                'onafterinitializing': self.onafterinitializing,
                'onafterresetting': self.onafterresetting,
                'onenterINIT': self.onenterinit,
                'onleaveINIT': self.onleaveinit,
                'onenterREADY': self.onenterready,
                'onenterERROR': self.onentererror,
                'onleaveERROR': self.onleaveerror,
                'onenterANIMATION': self.onenteranimation,
                'onleaveANIMATION': self.onleaveanimation,

                'onchangestate': self.printstatechange
            }
        })

    def printstatechange(self, event):
        """Executed on every state machine transition.
        """
        print('printstatechange; event: %s, %s->%s' % (event.event, event.src, event.dst))
        try:
            self.mqttclient.publish("{}/{}/events".format(self.config['MQTT']['TOPICBASE'],
                                                          self.config['CLIENTID']),
                                    event.event)
            self.mqttclient.publish("{}/{}/state".format(self.config['MQTT']['TOPICBASE'],
                                                         self.config['CLIENTID']),
                                    event.dst)
        except:
            pass

    def onbeforeinitializing(self, event):
        """Callback when triggering the event initializing()
        """
        print('onbeforeinitializing; event: %s, %s->%s' % (event.event, event.src, event.dst))

    def onafterinitializing(self, event):
        """Callback when finishing the event initializing()
        """
        print('onafterinitializing; event: %s, %s->%s' % (event.event, event.src, event.dst))

    def onafterresetting(self, event):
        """Callback when finishing the event resetting()
        """
        print('onafterresetting; event: %s, %s->%s' % (event.event, event.src, event.dst))

    def onenterinit(self, event):
        """Callback when entering the state INIT
        """
        print('onenterinit; event: %s, %s->%s' % (event.event, event.src, event.dst))

    def onleaveinit(self, event):
        """Callback when leaving the state INIT
        """
        print('onleaveinit; event: %s, %s->%s' % (event.event, event.src, event.dst))

    def onenterready(self, event):
        """Callback when entering the state READY
        """
        print('onenterready; event: %s, %s->%s' % (event.event, event.src, event.dst))

    def onleaveready(self, event):
        """Callback when leaving the state READY
        """
        print('onleaveready; event: %s, %s->%s' % (event.event, event.src, event.dst))

    def onentererror(self, event):
        """Callback when entering the state ERROR
        """
        print('onentererror; event: %s, %s->%s' % (event.event, event.src, event.dst))

    def onleaveerror(self, event):
        """Callback when leaving the state ERROR
        """
        #print(self.config)
        #try:
        #  self.mqttclient.publish(self.config['MQTT']['TOPICBASE'] + '/fsm/state', e.src + '->' + e.dst)
        #  self.mqttclient.disconnect()
        #  self.network.disconnect()
        #except:
        #  pass
        print('onleaveerror; event: %s, %s->%s' % (event.event, event.src, event.dst))

    def onenteranimation(self, event):
        """Callback when entering the state ANIMATION
        """
        print('onenteranimation; event: %s, %s->%s' % (event.event, event.src, event.dst))

    def onleaveanimation(self, event):
        """Callback when leaving the state ANIMATION
        """
        print('onleaveanimation; event: %s, %s->%s' % (event.event, event.src, event.dst))
