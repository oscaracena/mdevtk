#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import DJControlStarlight


class MyDJControl(DJControlStarlight):
    def __init__(self):
        super().__init__()
        self._l_color = (0, 0, 1)
        self._l_intensity = 125
        self._r_color = (0, 0, 1)
        self._r_intensity = 125
        self._blinking = False

    def _update(self):
        if self._blinking:
            return

        l_color = (
            self._l_color[0] * self._l_intensity,
            self._l_color[1] * self._l_intensity,
            self._l_color[2] * self._l_intensity
        )
        r_color = (
            self._r_color[0] * self._r_intensity,
            self._r_color[1] * self._r_intensity,
            self._r_color[2] * self._r_intensity
        )
        self.set_rgb_led(self.LEFT_BASE, *l_color)
        self.set_rgb_led(self.RIGHT_BASE, *r_color)

        msg = "< LEFT (r: {:03d}, g: {:03d}, b: {:03d})".format(*l_color)
        msg += ", RIGHT: (r: {:03d}, g: {:03d}, b: {:03d}) > ".format(*r_color)
        print("\r" + msg, end="")

    def _lerp(self, min_r, max_r, value):
        return int((1 - value) * min_r + value * max_r)

    def _value_to_color(self, value):
        normal_v = value / self.MAX_VALUE
        color = self._lerp(1, 7, normal_v)
        r = (color & 0b100) >> 2
        g = (color & 0b010) >> 1
        b = color & 0b001
        return (r, g, b)

    def on_left_bass(self, value):
        self._l_color = self._value_to_color(value)
        self._update()

    def on_right_bass(self, value):
        self._r_color = self._value_to_color(value)
        self._update()

    def on_left_volume(self, value):
        self._l_intensity = value * 255 // self.MAX_VALUE
        self._update()

    def on_right_volume(self, value):
        self._r_intensity = value * 255 // self.MAX_VALUE
        self._update()

    def on_left_hot_cue_1(self):
        self.set_rgb_led(self.BASE_BLINKING, 0, 0, 0)
        self._blinking = False
        self._update()

    def on_left_hot_cue_2(self):
        self.set_rgb_led(self.BASE_BLINKING, 0, 0, 255)
        self._blinking = True

try:
    device = MyDJControl()
    print("Use BASS knob to change bank color, VOLUME knob to change intensity.")
    print("Press Left HOT CUE 1 to switch off, and 2 to automatic blinking.\n")
    device._update()
    device.loop()
except KeyboardInterrupt:
    print("\b\b  \nBye!")
