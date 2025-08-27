#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2025, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import SMCPadPocket


class MySMCPadPocket(SMCPadPocket):
    def __init__(self):
        super().__init__(autoconnect=False)
        note_start = 22
        channel = 10
        self.connect(note_start, channel, ptype="momentary")
        self.sync()

        print("Setting up the controller (don't worry, changes are not persistent)...")

        # Change to Preset 1, Bank 1
        self.change_preset(1)
        self.change_bank(3)

        # Setup PADs to start on an specific note, channel and mode, and switch off the LEDs
        for pad in range(16):
            self.set_pad_mode(pad, "pad")
            self.set_pad_type(pad, "momentary")
            self.set_pad_note(pad, note_start + pad)
            self.set_pad_channel(pad, channel)
            self.led_off(pad)

    def on_pad(self, value, pad, row, col):
        if value:
            print(f"> PAD {pad} pressed! (row: {row}, col: {col})")


try:
    device = MySMCPadPocket()
    print("Ready! Press any PAD on your controller...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")
