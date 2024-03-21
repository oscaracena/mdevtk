#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import APCKey25MK2


class MyAPCKey25(APCKey25MK2):
    def on_shift(self):
        print("Shift KEY pressed!")


try:
    device = MyAPCKey25()
    print("Press the SHIFT button on your controller...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")
