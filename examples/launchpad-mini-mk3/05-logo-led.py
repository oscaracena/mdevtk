#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import time
from mdevtk import LaunchpadMiniMK3


class MyLaunchpadMiniMK3(LaunchpadMiniMK3):
    def __init__(self):
        super().__init__()
        self._color = 0

    def change_logo_color(self):
        self.led_on(self.LED_LOGO, self._color)
        self._color = (self._color + 1) & 0x7F


try:
    device = MyLaunchpadMiniMK3()
    print("You should see the Novation logo to change colors!")
    print("Press Ctrl+C to stop.")

    while True:
        device.change_logo_color()
        time.sleep(0.2)
except KeyboardInterrupt:
    device.close()
    print("\rBye!")
