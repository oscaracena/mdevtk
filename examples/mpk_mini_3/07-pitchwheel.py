#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import MPKMiniMK3


class MyMPKMiniMK3(MPKMiniMK3):
    def __init__(self):
        super().__init__()
        self._x = 0
        self._y = 0
        self._print_values()

    def _print_values(self):
        self._print_x()
        self._print_y()
        print("\033[3A")

    def on_y_axis(self, value):
        self._y = value
        self._print_values()

    def on_x_axis(self, value):
        # value ranges from -8192 to 8191, make it positive
        self._x = value + 8192
        self._print_values()

    def _print_x(self):
        width = 50
        perc = (self._x * 100) // 16383
        pos = (perc * width) // 100
        pos = min(width -1, pos)

        bar = list(" " * width)
        bar[width // 2] = "."
        bar[pos] = "#"
        bar = "".join(bar)
        print(f"- X-axis: {perc:3d}% \b |{bar}|")

    def _print_y(self):
        width = 50
        perc = (self._y * 100) // 127
        pos = (perc * width) // 100
        pos = min(width -1, pos)

        bar = list(" " * width)
        bar[width // 2] = "."
        bar[pos] = "#"
        bar = "".join(bar)
        print(f"- Y-axis: {perc:3d}% \b |{bar}|")


try:
    print("Press the PAD-1 on your controller...")
    device = MyMPKMiniMK3()
    device.loop()
except KeyboardInterrupt:
    print("\r- \n\nBye!")
