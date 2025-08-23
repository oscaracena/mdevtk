#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2025, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import SMCPadPocket


class MySMCPadPocket(SMCPadPocket):
    def on_pad(self, pad, row, col):
        print(f"PAD {pad} pressed! (row: {row}, col: {col})")


try:
    device = MySMCPadPocket()
    print("Press any PAD on your controller...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")
