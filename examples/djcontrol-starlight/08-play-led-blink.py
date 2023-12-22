#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import DJControlStarlight


class MyDJControl(DJControlStarlight):
    MAX_SPEED = 15
    EV_BLOCK  = 40

    def __init__(self):
        super().__init__()
        self.blinker = None
        self.speed = 3

        # count the events to reduce the wheel speed (i.e. 1 valid for each EV_BLOCK)
        self.ev_count = 0

    def on_left_play(self):
        if self.blinker is None:
            self.blinker = self.led_blink(self.LEFT_PLAY, speed=self.speed)
        else:
            self.blinker.stop()
            self.blinker = None

        self.print_status()

    def on_left_wheel_scratch(self, value):
        if value == 1:
            if self.ev_count < 0:
                self.ev_count = 0
            self.ev_count += 1
            if self.ev_count >= self.EV_BLOCK:
                self.ev_count = 0
                self.speed = min(self.MAX_SPEED, self.speed + 1)
        else:
            if self.ev_count > 0:
                self.ev_count = 0
            self.ev_count -= 1
            if self.ev_count <= -self.EV_BLOCK:
                self.ev_count = 0
                self.speed = max(1, self.speed -1)

        self.print_status()

        if self.blinker is not None:
            self.blinker.set_speed(self.speed)

    def print_status(self):
        status = "BLINKING" if self.blinker is not None else "  IDLE  "
        print(f"\r< PLAY status: {status}, speed: {self.speed} > ", end="")


try:
    device = MyDJControl()
    print("Press the left PLAY button to make it BLINK! Set its speed with the JOG WHEEL.")
    device.loop()
except KeyboardInterrupt:
    print("\b\b  \nBye!")
