#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import APCKey25MK2


class MyDJControl(APCKey25MK2):
    def __init__(self):
        super().__init__()
        self._max_value = 128
        self._curr_value = 64

    def on_knob_1(self, value):
        # NOTE: value < 64 -> CW, value > 64 CCW
        if value < 64:
            self._curr_value = min(self._max_value, self._curr_value + value)
        else:
            self._curr_value = max(1, self._curr_value + (value - 128))

        width = 50
        perc = (self._curr_value * 100) // self._max_value
        pos = (perc * width) // 100
        pos = min(width -1, pos)

        bar = list(" " * width)
        bar[width // 2] = "."
        bar[pos] = "#"
        bar = "".join(bar)

        print(f"\rKnob-1 pos: {perc:3d}% \b |{bar}| ", end="")


try:
    device = MyDJControl()
    print("Move the knob 1 (K1)...")
    device.loop()
except KeyboardInterrupt:
    print("\b\b  \nBye!")
