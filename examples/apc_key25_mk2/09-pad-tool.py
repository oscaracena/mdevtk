#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import time
from hexdump import hexdump
from mdevtk import APCKey25MK2


class MyAPCKey25(APCKey25MK2):
    DEF_COLOR = 5

    def __init__(self):
        super().__init__()
        self._bank = 0
        self._mode = self.LED_BRIGHT_50
        self._k1_cuml = 0
        self._selected = []

        self._update()

    def on_track_change(self, track_number):
        self._bank = track_number - 1
        self._update()

    def on_pad_pressed(self, pad):
        if self._bank > 4:
            return
        if self._bank == 4:
            if pad > len(self._selected):
                return
            color, mode = self._selected[pad - 1]
            color = self.COLORS[color]
            print(f" + COLOR: #{color:06X}, MODE: {mode}")
            return

        if self._bank == 3:
            color = self.DEF_COLOR
            if 1 <= pad < 9:
                mode = self._mode
                color = pad - 1 + (self._bank * 40)
            elif 17 <= pad < 24:
                mode = self.LED_BRIGHT_10 + (pad - 17)
            elif 25 <= pad < 29:
                mode = self.LED_PULSING_2 - (pad - 25)
            elif 33 <= pad < 38:
                mode = self.LED_BLINKING_2 - (pad - 33)
            else:
                return
        else:
            mode = self._mode
            color = pad - 1 + (self._bank * 40)

        self._selected.append((color, mode))
        color = self.COLORS[color]
        print(f" + COLOR: #{color:06X}, MODE: {mode}")

    def on_stop_all_clips(self):
        self._selected = []
        self._update()

    def on_knob_1(self, value):
        if value < 64:
            if self._k1_cuml < 0:
                self._k1_cuml = 0
            self._k1_cuml += value
        else:
            if self._k1_cuml > 0:
                self._k1_cuml = 0
            self._k1_cuml += (value - 128)

        if abs(self._k1_cuml) < 20:
            return

        if self._k1_cuml > 0:
            self._mode = min(self.LED_BRIGHT_100, self._mode + 1)
        else:
            self._mode = max(self.LED_BRIGHT_10, self._mode - 1)
        self._k1_cuml = 0
        self._update()

    def _update(self):
        # clear al pads
        for pad in range(40):
            self.led_off(pad)

        # show current bank colors
        for pad in range(40):
            color = pad + (self._bank * 40)
            if color >= 128:
                break
            self.set_pad_led(pad, color, self._mode)

        # show modes in bank 4
        if self._bank == 3:
            color = self.DEF_COLOR
            for i in range(7):
                mode = self.LED_BRIGHT_10 + i
                pad = self.PAD_17[1] + i
                self.set_pad_led(pad, color, mode)

            for i in range(4):
                mode = self.LED_PULSING_2 - i
                pad = self.PAD_25[1] + i
                self.set_pad_led(pad, color, mode)

            for i in range(5):
                mode = self.LED_BLINKING_2 - i
                pad = self.PAD_33[1] + i
                self.set_pad_led(pad, color, mode)

        # show selected pads in bank 5
        elif self._bank == 4:
            for pad, (color, mode) in enumerate(self._selected):
                self.set_pad_led(pad, color, mode)

        # update track buttons
        btn_track_1 = self.TRACK_1[1]
        for pad in range(8):
            self.led_off(btn_track_1 + pad)
        self.led_on(btn_track_1 + self._bank)


try:
    device = MyAPCKey25()
    print("Use track buttons to change page.")
    print("Use K1 to change brightness.")
    device.loop()
except KeyboardInterrupt:
    print("\b\b  \nBye!")
