#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import MPKMiniMK3


class MyMPKMiniMK3(MPKMiniMK3):
    def on_pad_1(self, bank):
        print(f"PAD 1 pressed! (bank: {bank})")


try:
    device = MyMPKMiniMK3()
    print("Press the PAD-1 on your controller...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")
