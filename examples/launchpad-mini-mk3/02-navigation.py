#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import LaunchpadMiniMK3
from utils import Cube


class MyLaunchpadMiniMK3(LaunchpadMiniMK3):
    def __init__(self):
        super().__init__()
        self._cube = Cube(20, 10)
        self._cube.show(False)

    def on_up(self):
        self._cube.up()

    def on_down(self):
        self._cube.down()

    def on_left(self):
        self._cube.left()

    def on_right(self):
        self._cube.right()


try:
    print("Press navigation buttons (up, down, left, right) on your controller...")
    device = MyLaunchpadMiniMK3()
    device.loop()
except KeyboardInterrupt:
    device.close()
    print("\rBye!")
