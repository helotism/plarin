# -*- coding: utf-8 -*-
"""
This modules provides code to animate an WS2812 led strip.
"""
import utime # pylint: disable=import-error
import machine # pylint: disable=import-error
import neopixel # pylint: disable=import-error

class Ledstrip:
    """For all components cofigured with this as the 'driver' an object of this class is created.

    Attributes:
        pin (int): The physical pin (not necessarily the printed number).
        pixels (int): How many LEDs are there on the strip.
    """

    def __init__(self, pin, pixels=8, rows=1):
        #
        self.logicalname = ""
        self.pin = pin
        self.pixels = pixels
        self.rows = rows
        self.patterns = ["NONE", "BLINK", "FADE",
                         "SCANNER_CA158", "SCANNER_CA190",
                         "CA30", "CA90", "BLINK_CA250"]
        self.pattern_active = "NONE"
        self.interval = 800
        self.ca_universe = ''
        self.ca_rule = {}
        self.ca_maxgenerations = 1
        self.ca_wraparoundcell = '0'
        self.last_update = utime.ticks_ms()
        self.color1 = (0, 0, 0)
        self.color2 = ()
        self.colors = {
            "off": (0, 0, 0),
            "on": (255, 255, 255)
        }
        self.colors_solarized = {
            "base03": (0, 43, 54),
            "base02": (7, 54, 66),
            "base01": (88, 110, 117),
            "base00": (101, 123, 131),
            "base0": (131, 148, 150),
            "base1": (147, 161, 161),
            "base2": (238, 232, 213),
            "base3": (253, 246, 227),
            "yellow": (181, 137, 0),
            "orange": (203, 75, 22),
            "red": (220, 50, 47),
            "magenta": (211, 54, 130),
            "violet": (108, 113, 196),
            "blue": (38, 139, 210),
            "cyan": (42, 161, 152),
            "green": (133, 153, 0)
        }
        self.total_steps = -1
        self.current_step = 0
        self.np = neopixel.NeoPixel(machine.Pin(self.pin), self.pixels)
        self.color1 = self.colors_solarized['red']
        self.color2 = self.colors_solarized['green']


    def update(self):

        if utime.ticks_diff(utime.ticks_ms(), self.last_update) > self.interval:

            self.last_update = utime.ticks_ms()

            if self.pattern_active in self.patterns:
                if self.pattern_active == "NONE":
                    for i in range(self.pixels):
                        self.np[i] = self.colors['off']
                    self.np.write()
                elif self.pattern_active == "BLINK":
                    #print("blink")
                    self.update_blink()
                elif self.pattern_active == "CA90":
                    self.update_ca90()
                elif self.pattern_active == "CA30":
                    self.update_ca30()
                else:
                    print("pattern not implemented yet.")
            else:
                print("wrong pattern")
        else:
            pass
            #print(utime.ticks_ms(), self.last_update, self.interval)

    #ToDo: Remove as this is only good for debugging
    def run(self):
        while True:
            #self.update_blink()
            self.update()
            #self.increment()
            utime.sleep_ms(self.interval)

    def increment(self):
        self.current_step += 1
        if self.current_step >= self.total_steps:
            self.current_step = 0

    def update_blink(self):
        for i in range(self.pixels):
            if i%2 == self.current_step%2:
                self.np[i] = self.color1
            else:
                self.np[i] = self.color2
        self.np.write()
        self.increment()

    def setup_blink(self):
        self.total_steps = 2

    def setup_ca30(self):
        self.ca_universe = ''
        for cell in range(self.pixels):
            if cell == (self.pixels // 2):
                self.ca_universe = self.ca_universe + "1"
            else:
                self.ca_universe = self.ca_universe + "0"
        neighbours2newstate_rule30 = {
            '000': '0',
            '001': '1',
            '010': '1',
            '011': '1',
            '100': '1',
            '101': '0',
            '110': '0',
            '111': '0'
        }
        self.ca_rule = neighbours2newstate_rule30

    def setup_ca90(self):
        self.ca_universe = ''
        for cell in range(self.pixels):
            if cell == (self.pixels // 2):
                self.ca_universe = self.ca_universe + "1"
            else:
                self.ca_universe = self.ca_universe + "0"
        neighbours2newstate_rule90 = {
            '000': '0',
            '001': '1',
            '010': '0',
            '011': '1',
            '100': '1',
            '101': '0',
            '110': '1',
            '111': '0'
        }
        self.ca_rule = neighbours2newstate_rule90

    #https://rosettacode.org/wiki/One-dimensional_cellular_automata# \
    #Python:_Straightforward_interpretation_of_spec
    def update_ca30(self):
        for i in range(self.ca_maxgenerations):
            for cell in range(self.pixels):
                if self.ca_universe[cell] == '0':
                    self.np[cell] = self.color1
                else:
                    self.np[cell] = self.color2
            self.np.write()
        #add a 0 on both ends
        self.ca_universe = self.ca_wraparoundcell + self.ca_universe + self.ca_wraparoundcell
        self.ca_universe = ''.join(self.ca_rule[self.ca_universe[i:i+3]] for i in range(self.pixels))

    def update_ca90(self):
        for i in range(self.ca_maxgenerations):
            for cell in range(self.pixels):
                if self.ca_universe[cell] == '0':
                    self.np[cell] = self.color1
                else:
                    self.np[cell] = self.color2
            self.np.write()
        #add a 0 on both ends
        self.ca_universe = self.ca_wraparoundcell + self.ca_universe + self.ca_wraparoundcell
        self.ca_universe = ''.join(self.ca_rule[self.ca_universe[i:i+3]] for i in range(self.pixels))
        #
