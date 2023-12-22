#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import DJControlStarlight


class MyDJControl(DJControlStarlight):
    def __init__(self):
        super().__init__()
        self.states = {}

    def toggle_led(self, led):
        state = not self.states.get(led, False)
        self.states[led] = state
        self.set_led(led, state)

    def on_left_sync(self):
        self.toggle_led(self.LEFT_SYNC)

    def on_left_cue(self):
        self.toggle_led(self.LEFT_CUE)

    def on_left_play(self):
        self.toggle_led(self.LEFT_PLAY)

    def on_left_headphones(self):
        self.toggle_led(self.LEFT_HEADPHONES)

    def on_vinyl(self):
        self.toggle_led(self.VINYL)

    def on_right_sync(self):
        self.toggle_led(self.RIGHT_SYNC)

    def on_right_cue(self):
        self.toggle_led(self.RIGHT_CUE)

    def on_right_play(self):
        self.toggle_led(self.RIGHT_PLAY)

    def on_right_headphones(self):
        self.toggle_led(self.RIGHT_HEADPHONES)

    def on_left_hot_cue_1(self):
        self.toggle_led(self.LEFT_PAD_1)

    def on_left_hot_cue_2(self):
        self.toggle_led(self.LEFT_PAD_2)

    def on_left_hot_cue_3(self):
        self.toggle_led(self.LEFT_PAD_3)

    def on_left_hot_cue_4(self):
        self.toggle_led(self.LEFT_PAD_4)

    def on_right_hot_cue_1(self):
        self.toggle_led(self.RIGHT_PAD_1)

    def on_right_hot_cue_2(self):
        self.toggle_led(self.RIGHT_PAD_2)

    def on_right_hot_cue_3(self):
        self.toggle_led(self.RIGHT_PAD_3)

    def on_right_hot_cue_4(self):
        self.toggle_led(self.RIGHT_PAD_4)


try:
    device = MyDJControl()
    print("Press any LED button to change its state...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")
