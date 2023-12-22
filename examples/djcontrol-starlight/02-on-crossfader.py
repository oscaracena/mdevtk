#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import DJControlStarlight


class MyDJControl(DJControlStarlight):
    def on_crossfader_slide(self, value):
        width = 50
        perc = (value * 100) // self.MAX_VALUE
        pos = (perc * width) // 100
        pos = min(width -1, pos)

        bar = list(" " * width)
        bar[width // 2] = "."
        bar[pos] = "#"
        bar = "".join(bar)

        print(f"\rCrossfade pos: {perc:3d}% \b |{bar}| ", end="")


try:
    device = MyDJControl()
    print("Move the crossfade (the central slider)...")
    device.loop()
except KeyboardInterrupt:
    print("\b\b  \nBye!")
