#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import time
from mdevtk import APCKey25MK2


class MyAPCKey25(APCKey25MK2):
    def __init__(self):
        super().__init__()
        self.color = 0

    def on_up(self):
        self.color = min(127, self.color + 1)
        self._update()

    def on_down(self):
        self.color = max(0, self.color - 1)
        self._update()

    def _update(self):
        color = self.COLORS[self.color]
        r = (color >> 16) & 0xff
        g = (color >> 8) & 0xff
        b = color & 0xff
        self.set_rgb_led(self.PAD_1, r, g, b)
        print(f"\r< COLOR value: 0x{color:06x} > ", end="")

try:
    device = MyAPCKey25()
    print("Press UP and DOWN to change PAD 1 LED color...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\b\b  \nBye!")
