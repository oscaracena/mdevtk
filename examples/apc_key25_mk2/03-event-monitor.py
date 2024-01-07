#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import APCKey25MK2


class MyAPCKey25(APCKey25MK2):
    # NOTE: instead of overriding 'on_clip_N()', you can use 'on_clip(n)'
    def on_clip_change(self, number):
        print(f"clip number: {number}")

    # def on_clip_1(self):
    #     print("clip 1")

    # def on_clip_2(self):
    #     print("clip 2")

    def on_clip_3(self):
        print("clip 3")

    def on_clip_4(self):
        print("clip 4")

    def on_clip_5(self):
        print("clip 5")

    def on_clip_6(self):
        print("clip 6")

    def on_clip_7(self):
        print("clip 7")

    def on_clip_8(self):
        print("clip 8")

    def on_clip_9(self):
        print("clip 9")

    def on_clip_10(self):
        print("clip 10")

    def on_clip_11(self):
        print("clip 11")

    def on_clip_12(self):
        print("clip 12")

    def on_clip_13(self):
        print("clip 13")

    def on_clip_14(self):
        print("clip 14")

    def on_clip_15(self):
        print("clip 15")

    def on_clip_16(self):
        print("clip 16")

    def on_clip_17(self):
        print("clip 17")

    def on_clip_18(self):
        print("clip 18")

    def on_clip_19(self):
        print("clip 19")

    def on_clip_20(self):
        print("clip 20")

    def on_clip_21(self):
        print("clip 21")

    def on_clip_22(self):
        print("clip 22")

    def on_clip_23(self):
        print("clip 23")

    def on_clip_24(self):
        print("clip 24")

    def on_clip_25(self):
        print("clip 25")

    def on_clip_26(self):
        print("clip 26")

    def on_clip_27(self):
        print("clip 27")

    def on_clip_28(self):
        print("clip 28")

    def on_clip_29(self):
        print("clip 29")

    def on_clip_30(self):
        print("clip 30")

    def on_clip_31(self):
        print("clip 31")

    def on_clip_32(self):
        print("clip 32")

    def on_clip_33(self):
        print("clip 33")

    def on_clip_34(self):
        print("clip 34")

    def on_clip_35(self):
        print("clip 35")

    def on_clip_36(self):
        print("clip 36")

    def on_clip_37(self):
        print("clip 37")

    def on_clip_38(self):
        print("clip 38")

    def on_clip_39(self):
        print("clip 39")

    def on_clip_40(self):
        print("clip 40")

    def on_up(self):
        print("up")

    def on_down(self):
        print("down")

    def on_left(self):
        print("left")

    def on_right(self):
        print("right")

    def on_knob_ctrl_volume(self):
        print("knob_ctrl_volume")

    def on_knob_ctrl_pan(self):
        print("knob_ctrl_pan")

    def on_knob_ctrl_send(self):
        print("knob_ctrl_send")

    def on_knob_ctrl_device(self):
        print("knob_ctrl_device")

    def on_stop_all_clips(self):
        print("stop_all_clips")

    def on_soft_key_clip_stop(self):
        print("soft_key_clip_stop")

    def on_soft_key_solo(self):
        print("soft_key_solo")

    def on_soft_key_mute(self):
        print("soft_key_mute")

    def on_soft_key_rec_arm(self):
        print("soft_key_rec_arm")

    def on_soft_key_select(self):
        print("soft_key_select")

    def on_play(self):
        print("play")

    def on_rec(self):
        print("rec")

    def on_shift(self):
        print("shift")

    def on_knob_1(self, value):
        print(f"knob 1, value: {value}")

    def on_knob_2(self, value):
        print(f"knob 2, value: {value}")

    def on_knob_3(self, value):
        print(f"knob 3, value: {value}")

    def on_knob_4(self, value):
        print(f"knob 4, value: {value}")

    def on_knob_5(self, value):
        print(f"knob 5, value: {value}")

    def on_knob_6(self, value):
        print(f"knob 6, value: {value}")

    def on_knob_7(self, value):
        print(f"knob 7, value: {value}")

    def on_knob_8(self, value):
        print(f"knob 8, value: {value}")


try:
    device = MyAPCKey25()
    print("Press any button, key or knob...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")
