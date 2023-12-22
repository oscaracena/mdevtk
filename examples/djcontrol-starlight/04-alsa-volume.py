#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import sys
from mdevtk import DJControlStarlight
try:
    import alsaaudio
except ImportError:
    print("Sorry, you need pyalsaaudio installed. Try with 'pip install pyalsaaudio'.")
    sys.exit(-1)


class MyDJControl(DJControlStarlight):
    def __init__(self):
        super().__init__()
        self.mixer = alsaaudio.Mixer()

    def on_master_gain(self, value):
        vol = (value * 100) // self.MAX_VALUE
        self.mixer.setvolume(vol)

        blocks = (vol // 2)
        bar = "#" * blocks + " " * (50 - blocks)
        print(f"\rVolume change to {vol:3d}% \b |{bar}| ", end="")


try:
    device = MyDJControl()
    print("Press the master gain knob to control your system's volume...")
    device.loop()
except KeyboardInterrupt:
    print("\b\b  \nBye!")
