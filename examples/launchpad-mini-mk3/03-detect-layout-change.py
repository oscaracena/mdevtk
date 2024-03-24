#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import LaunchpadMiniMK3


class MyLaunchpadMiniMK3(LaunchpadMiniMK3):
    def on_session_mode(self):
        print(f" - LAYOUT switch to Session.")

    def on_drums_mode(self):
        print(f" - LAYOUT switch to Drums.")

    def on_keys_mode(self):
        print(f" - LAYOUT switch to Keys.")

    def on_user_mode(self):
        print(f" - LAYOUT switch to User.")


try:
    device = MyLaunchpadMiniMK3()
    print("Change the Launchpad layout, pressing Drums, Keys or User buttons...")
    device.loop()
except KeyboardInterrupt:
    device.close()
    print("\rBye!")
