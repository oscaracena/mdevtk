#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2025, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from random import randrange
from mdevtk import SMCPadPocket


class MySMCPadPocket(SMCPadPocket):
    def __init__(self):
        super().__init__()
        note_start = 0
        channel = 0
        super().__init__(note_start, channel)
        self.sync()

        print("Setting up the controller (don't worry, changes are not persistent)...")

        # Change to Preset 1, Bank 1
        self.change_preset(0)
        self.change_bank(0)
        self.color = (0, 0, 0)

        # Setup PADs to start on an specific note, channel and mode, and switch off the LEDs
        for pad in range(16):
            self.set_pad_mode(pad, "pad")
            self.set_pad_type(pad, "note")
            self.set_pad_note(pad, note_start + pad)
            self.set_pad_channel(pad, channel)
            self.led_off(pad)

    def on_pad(self, pad, row, col):
        self._update_color()
        self.set_rgb_led(pad, *self.color)

    def _update_color(self):
        self.color = (randrange(0, 255), randrange(0, 255), randrange(0, 255))

try:
    device = MySMCPadPocket()
    print("Ready! Press any PAD on your controller...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")

