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
        self.toggle_led(self.LEFT_HOT_CUE_1)

    def on_left_hot_cue_2(self):
        self.toggle_led(self.LEFT_HOT_CUE_2)

    def on_left_hot_cue_3(self):
        self.toggle_led(self.LEFT_HOT_CUE_3)

    def on_left_hot_cue_4(self):
        self.toggle_led(self.LEFT_HOT_CUE_4)

    def on_left_loop_1(self):
        self.toggle_led(self.LEFT_LOOP_1)

    def on_left_loop_2(self):
        self.toggle_led(self.LEFT_LOOP_2)

    def on_left_loop_3(self):
        self.toggle_led(self.LEFT_LOOP_3)

    def on_left_loop_4(self):
        self.toggle_led(self.LEFT_LOOP_4)

    def on_left_fx_1(self):
        self.toggle_led(self.LEFT_FX_1)

    def on_left_fx_2(self):
        self.toggle_led(self.LEFT_FX_2)

    def on_left_fx_3(self):
        self.toggle_led(self.LEFT_FX_3)

    def on_left_fx_4(self):
        self.toggle_led(self.LEFT_FX_4)

    def on_left_sampler_1(self):
        self.toggle_led(self.LEFT_SAMPLER_1)

    def on_left_sampler_2(self):
        self.toggle_led(self.LEFT_SAMPLER_2)

    def on_left_sampler_3(self):
        self.toggle_led(self.LEFT_SAMPLER_3)

    def on_left_sampler_4(self):
        self.toggle_led(self.LEFT_SAMPLER_4)

    def on_right_hot_cue_1(self):
        self.toggle_led(self.RIGHT_HOT_CUE_1)

    def on_right_hot_cue_2(self):
        self.toggle_led(self.RIGHT_HOT_CUE_2)

    def on_right_hot_cue_3(self):
        self.toggle_led(self.RIGHT_HOT_CUE_3)

    def on_right_hot_cue_4(self):
        self.toggle_led(self.RIGHT_HOT_CUE_4)

    def on_right_loop_1(self):
        self.toggle_led(self.RIGHT_LOOP_1)

    def on_right_loop_2(self):
        self.toggle_led(self.RIGHT_LOOP_2)

    def on_right_loop_3(self):
        self.toggle_led(self.RIGHT_LOOP_3)

    def on_right_loop_4(self):
        self.toggle_led(self.RIGHT_LOOP_4)

    def on_right_fx_1(self):
        self.toggle_led(self.RIGHT_FX_1)

    def on_right_fx_2(self):
        self.toggle_led(self.RIGHT_FX_2)

    def on_right_fx_3(self):
        self.toggle_led(self.RIGHT_FX_3)

    def on_right_fx_4(self):
        self.toggle_led(self.RIGHT_FX_4)

    def on_right_sampler_1(self):
        self.toggle_led(self.RIGHT_SAMPLER_1)

    def on_right_sampler_2(self):
        self.toggle_led(self.RIGHT_SAMPLER_2)

    def on_right_sampler_3(self):
        self.toggle_led(self.RIGHT_SAMPLER_3)

    def on_right_sampler_4(self):
        self.toggle_led(self.RIGHT_SAMPLER_4)

try:
    device = MyDJControl()
    print("Press any LED button to change its state...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")
