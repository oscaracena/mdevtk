#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2025, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import SMCPadPocket


class MySMCPadPocket(SMCPadPocket):
    def __init__(self):
        super().__init__()
        # self.color = 0

    def on_pad(self, pad, row, col):
        # self.color = (self.color + 1) % 127
        self.set_rgb_led(pad, 255, 0, 0, bank=2)

try:
    device = MySMCPadPocket()
    print("Press any PAD on your controller...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")

