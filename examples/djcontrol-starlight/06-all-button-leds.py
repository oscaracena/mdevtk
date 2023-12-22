#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import time
from mdevtk import DJControlStarlight


class MyDJControl(DJControlStarlight):
    def __init__(self):
        super().__init__()
        self.set_all_leds(True)

    def set_all_leds(self, state):
        all_leds = [
            self.LEFT_SYNC,
            self.LEFT_CUE,
            self.LEFT_PLAY,
            self.LEFT_HEADPHONES,
            self.LEFT_PAD_1,
            self.LEFT_PAD_2,
            self.LEFT_PAD_3,
            self.LEFT_PAD_4,
            self.RIGHT_SYNC,
            self.RIGHT_CUE,
            self.RIGHT_PLAY,
            self.RIGHT_HEADPHONES,
            self.RIGHT_VINYL,
            self.RIGHT_PAD_1,
            self.RIGHT_PAD_2,
            self.RIGHT_PAD_3,
            self.RIGHT_PAD_4,
        ]

        for led in all_leds:
            self.set_led(led, state)


try:
    device = MyDJControl()
    print("Now, you should see all controller LEDs on...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    device.set_all_leds(False)
    print("\rBye!")
