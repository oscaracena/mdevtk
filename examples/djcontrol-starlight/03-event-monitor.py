#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import DJControlStarlight


class MyDJControl(DJControlStarlight):
    def on_bass_filter_toggle(self):
        print("bass filter toggle")

    def on_shift(self):
        print("shift")

    def on_left_sync(self):
        print("left sync")

    def on_left_cue(self):
        print("left cue")

    def on_left_play(self):
        print("left play")

    def on_left_wheel_touch(self):
        print("left wheel touch")

    def on_left_headphones(self):
        print("left headphones")

    def on_left_hot_cue(self):
        print("left hot cue")

    def on_left_loop(self):
        print("left loop")

    def on_left_fx(self):
        print("left fx")

    def on_left_sampler(self):
        print("left sampler")

    def on_vinyl(self):
        print("vinyl")

    def on_right_sync(self):
        print("right sync")

    def on_right_cue(self):
        print("right cue")

    def on_right_play(self):
        print("right play")

    def on_right_wheel_touch(self):
        print("right wheel touch")

    def on_right_headphones(self):
        print("right headphones")

    def on_right_hot_cue(self):
        print("right hot cue")

    def on_right_loop(self):
        print("right loop")

    def on_right_fx(self):
        print("right fx")

    def on_right_sampler(self):
        print("right sampler")

    def on_left_sync_off(self):
        print("left sync off")

    def on_left_prev_track(self):
        print("left prev track")

    def on_left_stutter(self):
        print("left stutter")

    def on_cue_master(self):
        print("cue master")

    def on_right_sync_off(self):
        print("right sync off")

    def on_right_prev_track(self):
        print("right prev track")

    def on_right_stutter(self):
        print("right stutter")

    def on_cue_mix(self):
        print("cue mix")

    def on_left_hot_cue_1(self):
        print("left hot cue 1")

    def on_left_hot_cue_2(self):
        print("left hot cue 2")

    def on_left_hot_cue_3(self):
        print("left hot cue 3")

    def on_left_hot_cue_4(self):
        print("left hot cue 4")

    def on_left_loop_1(self):
        print("left loop 1")

    def on_left_loop_2(self):
        print("left loop 2")

    def on_left_loop_3(self):
        print("left loop 3")

    def on_left_loop_4(self):
        print("left loop 4")

    def on_left_fx_1(self):
        print("left fx 1")

    def on_left_fx_2(self):
        print("left fx 2")

    def on_left_fx_3(self):
        print("left fx 3")

    def on_left_fx_4(self):
        print("left fx 4")

    def on_left_sampler_1(self):
        print("left sampler 1")

    def on_left_sampler_2(self):
        print("left sampler 2")

    def on_left_sampler_3(self):
        print("left sampler 3")

    def on_left_sampler_4(self):
        print("left sampler 4")

    def on_right_hot_cue_1(self):
        print("right hot cue 1")

    def on_right_hot_cue_2(self):
        print("right hot cue 2")

    def on_right_hot_cue_3(self):
        print("right hot cue 3")

    def on_right_hot_cue_4(self):
        print("right hot cue 4")

    def on_right_loop_1(self):
        print("right loop 1")

    def on_right_loop_2(self):
        print("right loop 2")

    def on_right_loop_3(self):
        print("right loop 3")

    def on_right_loop_4(self):
        print("right loop 4")

    def on_right_fx_1(self):
        print("right fx 1")

    def on_right_fx_2(self):
        print("right fx 2")

    def on_right_fx_3(self):
        print("right fx 3")

    def on_right_fx_4(self):
        print("right fx 4")

    def on_right_sampler_1(self):
        print("right sampler 1")

    def on_right_sampler_2(self):
        print("right sampler 2")

    def on_right_sampler_3(self):
        print("right sampler 3")

    def on_right_sampler_4(self):
        print("right sampler 4")

    def on_crossfader_slide(self, value):
        print(f"crossfader slide, value: {value}")

    def on_master_gain(self, value):
        print(f"master gain, value: {value}")

    def on_headphones_gain(self, value):
        print(f"headphones gain, value: {value}")

    def on_left_volume(self, value):
        print(f"left volume, value: {value}")

    def on_left_bass(self, value):
        print(f"left bass, value: {value}")

    def on_left_filter(self, value):
        print(f"left filter, value: {value}")

    def on_left_tempo_slide(self, value):
        print(f"left tempo slide, value: {value}")

    def on_left_wheel_transport(self, value):
        print(f"left wheel transport, value: {value}")

    def on_left_wheel_scratch(self, value):
        print(f"left wheel scratch, value: {value}")

    def on_right_volume(self, value):
        print(f"right volume, value: {value}")

    def on_right_bass(self, value):
        print(f"right bass, value: {value}")

    def on_right_filter(self, value):
        print(f"right filter, value: {value}")

    def on_right_tempo_slide(self, value):
        print(f"right tempo slide, value: {value}")

    def on_right_wheel_transport(self, value):
        print(f"right wheel transport, value: {value}")

    def on_right_wheel_scratch(self, value):
        print(f"right wheel scratch, value: {value}")


try:
    device = MyDJControl()
    print("Press any button, slider or control element...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")
