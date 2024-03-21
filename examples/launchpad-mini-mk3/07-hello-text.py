#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import LaunchpadMiniMK3


try:
    print("Read the Launchpad, not here! ;)")
    device = LaunchpadMiniMK3()
    device.print("Hello World!", speed=6)
    device.loop()
except KeyboardInterrupt:
    device.print_clear()
    device.close()
    print("\rBye!")
