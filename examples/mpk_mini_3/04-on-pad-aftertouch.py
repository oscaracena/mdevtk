#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import MPKMiniMK3


class MyMPKMiniMK3(MPKMiniMK3):
    def on_pad_aftertouch(self, value):
        print(f"\r- PAD aftertouch! (value: {value:-3d})\r", end="")


try:
    device = MyMPKMiniMK3()
    print("Press any PAD on your controller, and then change the pressure...")
    device.loop()
except KeyboardInterrupt:
    print("\r- \nBye!")
