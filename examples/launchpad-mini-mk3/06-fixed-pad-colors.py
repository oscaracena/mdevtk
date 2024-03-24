#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import LaunchpadMiniMK3


class MyLaunchpadMiniMK3(LaunchpadMiniMK3):
    def __init__(self):
        super().__init__()
        self.on_left()

    def on_left(self):
        self._fill(0)
        self.led_off(self.LED_RIGHT)
        self.led_on(self.LED_LEFT, color=9)

    def on_right(self):
        self._fill(64)
        self.led_off(self.LED_LEFT)
        self.led_on(self.LED_RIGHT, color=9)

    def _fill(self, start):
        color = start
        for row in range(1, 9):
            for col in range(1, 9):
                led = row * 10 + col
                self.led_on(led, color=color)
                color = min(127, color + 1)


try:
    device = MyLaunchpadMiniMK3()
    print("You should see all available colors in pads. Switch between pages using")
    print("left and right arrows. Ctrl+C to stop.")
    device.loop()
except KeyboardInterrupt:
    device.close()
    print("\rBye!")
