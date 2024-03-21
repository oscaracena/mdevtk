#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import LaunchpadMiniMK3


class MyLaunchpadMiniMK3(LaunchpadMiniMK3):
    pass


try:
    device = MyLaunchpadMiniMK3()
    print("")
    device.loop()
except KeyboardInterrupt:
    device.close()
    print("\rBye!")
