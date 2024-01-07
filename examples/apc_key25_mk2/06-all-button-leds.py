#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import time
from mdevtk import APCKey25MK2


class MyAPCKey25(APCKey25MK2):
    def __init__(self):
        super().__init__()
        self.set_all_leds(True)

    def set_all_leds(self, state):
        normal_leds = [
            self.LED_UP,
            self.LED_LED_DOWN,
            self.LED_LEFT,
            self.LED_RIGHT,
            self.LED_VOLUME,
            self.LED_PAN,
            self.LED_SEND,
            self.LED_DEVICE,
            self.LED_CLIP_STOP,
            self.LED_SOLO,
            self.LED_MUTE,
            self.LED_REC_ARM,
            self.LED_SELECT,
        ]

        for led in normal_leds:
            self.set_led(led, state)

        rgb_leds = [getattr(self, f"PAD_{i}") for i in  range(1, 41)]
        for led in rgb_leds:
            color = (0, 0, 0) if not state else (2, 0, 0)
            self.set_rgb_led(led, *color)

try:
    device = MyAPCKey25()
    print("Now, you should see all controller LEDs on...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    device.set_all_leds(False)
    print("\rBye!")
