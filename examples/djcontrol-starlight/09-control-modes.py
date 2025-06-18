#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import DJControlStarlight


class MyDJControl(DJControlStarlight):
    def set_mode(self, mode):
        mode = mode.lower()[:2]
        if len(mode) != 2 or mode[0] not in "ab" or mode[1] not in "1234":
            print("ERROR: Invalid mode!")
            return

        mode_name = "LEFT" if mode[0] == "a" else "RIGHT"
        mode_name += "_MODE_"
        mode_name += ["HOT_CUE", "LOOP", "FX", "SAMPLER"][int(mode[1])-1]
        super().change_bank(getattr(self, mode_name))


try:
    device = MyDJControl()
    print("Insert here the deck mode that you want to set.")
    print("Format: 'XY' where")
    print("  - X is 'A' or 'B' (the choosen deck)")
    print("  - Y is a number, 1: HOT CUE, 2: LOOP, 3: FX and 4: SAMPLER")
    while True:
        mode = input("CMD> ")
        device.set_mode(mode)
except KeyboardInterrupt:
    print("\b\b  \nBye!")
