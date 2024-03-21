#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import MPKMiniMK3


class MyMPKMiniMK3(MPKMiniMK3):
    def on_knob_1(self, value):
        width = 50
        perc = (value * 100) // 127
        pos = (perc * width) // 100
        pos = min(width -1, pos)

        bar = list(" " * width)
        bar[width // 2] = "."
        bar[pos] = "#"
        bar = "".join(bar)

        print(f"\rKnob-1 pos: {perc:3d}% \b |{bar}| ", end="")


try:
    device = MyMPKMiniMK3()
    print("Move the knob 1 (K1)...")
    device.loop()
except KeyboardInterrupt:
    print("\b\b  \nBye!")
