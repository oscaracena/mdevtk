#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import DJControlStarlight


class MyDJControl(DJControlStarlight):
    def __init__(self):
        super().__init__()
        self.is_on = False

    def on_left_play(self):
        if self.is_on:
            self.led_off(self.LEFT_PLAY)
        else:
            self.led_on(self.LEFT_PLAY)

        self.is_on = not self.is_on
        status = " ON" if self.is_on else "OFF"
        print(f"\r< PLAY pressed, status: {status} > ", end="")


try:
    device = MyDJControl()
    print("Press the left PLAY button to change its LED status...")
    device.loop()
except KeyboardInterrupt:
    print("\b\b  \nBye!")
