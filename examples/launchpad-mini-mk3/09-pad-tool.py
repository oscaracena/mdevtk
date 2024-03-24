#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import LaunchpadMiniMK3


class MyLaunchpadMiniMK3(LaunchpadMiniMK3):
    DEF_COLOR = 5

    def __init__(self):
        super().__init__()
        self._bank = 0
        self._selected = []
        self._is_remove_mode = False
        self._update()

    def on_session(self, num):
        if num == 0:
            self._is_remove_mode ^= True
        elif 5 <= num <= 7:
            self._bank = 7 - num
        else:
            return
        self._update()

    def on_pad(self, pad, row, col):
        if self._bank > 2:
            return

        if self._bank == 2:
            if pad > len(self._selected):
                return
            color = self._selected[pad]
            if color is None:
                return
            print(f" + COLOR, vel: {color} 0x{color:02X}, pad: {pad}")

            if self._is_remove_mode:
                self._selected[pad] = None
                self._update()
            return

        color = pad + 64 * self._bank

        try:
            hole = self._selected.index(None)
            self._selected[hole] = color
        except ValueError:
            self._selected.append(color)

        print(f" + COLOR, vel: {color} 0x{color:02X}, pad: {pad}")

    def all_off(self):
        for row in range(1, 10):
            for col in range(1, 10):
                pad = row * 10 + col
                self.led_off(pad)

    def _update(self):
        self.all_off()

        # show selected pads in bank 2
        if self._bank == 2:
            for pad, color in enumerate(self._selected):
                if color is None:
                    continue
                note = 11 + pad + (pad // 8) * 2
                self.led_on(note, color)

        # show current bank colors
        elif self._bank < 2:
            color = 64 * self._bank
            for row in range(1, 9):
                for col in range(1, 9):
                    pad = row * 10 + col
                    self.led_on(pad, color=color)
                    color = min(127, color + 1)

        # update session buttons
        selected = self.LED_SESSION_END - 10 * self._bank
        self.led_on(selected, color=41)

        if self._is_remove_mode:
            self.led_on(self.LED_STOP, color=5)


try:
    device = MyLaunchpadMiniMK3()
    print("Use session buttons to change page (page 3 is your selection).")
    print("Press Stop/Solo/Mute to enter delete mode (for page 3)")
    device.loop()
except KeyboardInterrupt:
    device.close()
    print("\b\b  \nBye!")
