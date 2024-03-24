#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import LaunchpadMiniMK3


class MyLaunchpadMiniMK3(LaunchpadMiniMK3):
    def __init__(self):
        super().__init__()
        self.setup_faders(vertical=True, faders=[
            {"cc": 23, "name": "my_fader"},
            None,
            {"cc": 55, "name": "volume", "color": 5},
            {"cc": 56, "name": "pan", "color": 21, "bipolar": True},
        ])
        self.show_faders()

    def on_session_mode(self):
        self.show_faders()

    def on_up(self):
        self.hide_faders()

    def on_my_fader_change(self, value):
        print(f" - FADER changed to {value}")

    def on_volume_change(self, value):
        print(f" - Volume set to {value}")

    def on_pan_change(self, value):
        print(f" - pan set to {value}")


try:
    device = MyLaunchpadMiniMK3()
    print("Change the faders value pressing one of their PADs.")
    device.loop()
except KeyboardInterrupt:
    device.close()
    print("\rBye!")
