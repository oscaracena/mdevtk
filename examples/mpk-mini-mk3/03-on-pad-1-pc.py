#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import MPKMiniMK3


class MyMPKMiniMK3(MPKMiniMK3):
    def on_pad_1_pc(self, program, bank):
        print(f"\r- PAD 1 program change! (program: {program}, bank: {bank})\r", end="")


try:
    device = MyMPKMiniMK3()
    print("Set PROG CHANGE mode in PAD CONTROLS and then press the PAD-1 on your controller...")
    device.loop()
except KeyboardInterrupt:
    print("\r- \nBye!")
