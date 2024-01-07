#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import time
from mdevtk import APCKey25MK2


class MyAPCKey25(APCKey25MK2):
    def __init__(self):
        super().__init__()
        self.r = 0
        self.g = 0
        self.b = 0

    def on_knob_1(self, v):
        self.r += v if v < 64 else (v - 128)
        self.r = max(0, min(255, self.r))
        self._update()

    def on_knob_2(self, v):
        self.g += v if v < 64 else (v - 128)
        self.g = max(0, min(255, self.g))
        self._update()

    def on_knob_3(self, v):
        self.b += v if v < 64 else (v - 128)
        self.b = max(0, min(255, self.b))
        self._update()

    def _update(self):
        c = (self.r << 16) + (self.g << 8) + self.b
        self.set_rgb_led(self.PAD_1, self.r, self.g, self.b)
        print(f"\r< COLOR value: 0x{c:06x} > ", end="")

try:
    device = MyAPCKey25()
    print("Move kobs 1-3 to change LED color. K1=Red, K2=Green, K3=Blue...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\b\b  \nBye!")
