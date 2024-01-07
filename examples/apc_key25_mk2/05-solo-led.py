#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import APCKey25MK2


class MyAPCKey25(APCKey25MK2):
    def __init__(self):
        super().__init__()
        self.is_on = False

    def on_soft_key_solo(self):
        if self.is_on:
            self.led_off(self.LED_SOLO)
        else:
            self.led_on(self.LED_SOLO)

        self.is_on = not self.is_on
        status = " ON" if self.is_on else "OFF"
        print(f"\r< PLAY pressed, status: {status} > ", end="")


try:
    device = MyAPCKey25()
    print("Press the soft key SOLO (scene 2) to change its LED status...")
    device.loop()
except KeyboardInterrupt:
    print("\b\b  \nBye!")
