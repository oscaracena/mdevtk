#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import sys
from mdevtk import APCKey25MK2
try:
    import alsaaudio
except ImportError:
    print("Sorry, you need pyalsaaudio installed. Try with 'pip install pyalsaaudio'.")
    sys.exit(-1)


class MyAPCKey25(APCKey25MK2):
    def __init__(self):
        super().__init__()
        self.mixer = alsaaudio.Mixer()
        self.volume = self.mixer.getvolume()[0]

    def on_knob_1(self, value):
        # NOTE: value < 64 -> CW, value > 64 CCW
        if value < 64:
            self.volume = min(100, self.volume + value)
        else:
            self.volume = max(0, self.volume + (value - 128))

        self.mixer.setvolume(self.volume)

        blocks = (self.volume // 2)
        bar = "#" * blocks + " " * (50 - blocks)
        print(f"\rVolume change to {self.volume:3d}% \b |{bar}| ", end="")


try:
    device = MyAPCKey25()
    print("Rotate the knob 1 to control your system's volume...")
    device.loop()
except KeyboardInterrupt:
    print("\b\b  \nBye!")
