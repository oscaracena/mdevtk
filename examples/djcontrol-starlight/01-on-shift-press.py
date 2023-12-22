#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import DJControlStarlight


class MyDJControl(DJControlStarlight):
    def on_shift(self):
        print("Shift KEY pressed!")


try:
    device = MyDJControl()
    print("Press the SHIFT button on your DJControl...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")
