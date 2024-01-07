#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import APCKey25MK2


class MyAPCKey25(APCKey25MK2):
    # NOTE: instead of overriding 'on_pad_N()', you can use 'on_pad_pressed(n)'
    def on_pad_pressed(self, number):
        print(f"pad number: {number}")

    # def on_pad_1(self):
    #     print("pad 1")

    # def on_pad_2(self):
    #     print("pad 2")

    def on_pad_3(self):
        print("pad 3")

    def on_pad_4(self):
        print("pad 4")

    def on_pad_5(self):
        print("pad 5")

    def on_pad_6(self):
        print("pad 6")

    def on_pad_7(self):
        print("pad 7")

    def on_pad_8(self):
        print("pad 8")

    def on_pad_9(self):
        print("pad 9")

    def on_pad_10(self):
        print("pad 10")

    def on_pad_11(self):
        print("pad 11")

    def on_pad_12(self):
        print("pad 12")

    def on_pad_13(self):
        print("pad 13")

    def on_pad_14(self):
        print("pad 14")

    def on_pad_15(self):
        print("pad 15")

    def on_pad_16(self):
        print("pad 16")

    def on_pad_17(self):
        print("pad 17")

    def on_pad_18(self):
        print("pad 18")

    def on_pad_19(self):
        print("pad 19")

    def on_pad_20(self):
        print("pad 20")

    def on_pad_21(self):
        print("pad 21")

    def on_pad_22(self):
        print("pad 22")

    def on_pad_23(self):
        print("pad 23")

    def on_pad_24(self):
        print("pad 24")

    def on_pad_25(self):
        print("pad 25")

    def on_pad_26(self):
        print("pad 26")

    def on_pad_27(self):
        print("pad 27")

    def on_pad_28(self):
        print("pad 28")

    def on_pad_29(self):
        print("pad 29")

    def on_pad_30(self):
        print("pad 30")

    def on_pad_31(self):
        print("pad 31")

    def on_pad_32(self):
        print("pad 32")

    def on_pad_33(self):
        print("pad 33")

    def on_pad_34(self):
        print("pad 34")

    def on_pad_35(self):
        print("pad 35")

    def on_pad_36(self):
        print("pad 36")

    def on_pad_37(self):
        print("pad 37")

    def on_pad_38(self):
        print("pad 38")

    def on_pad_39(self):
        print("pad 39")

    def on_pad_40(self):
        print("pad 40")

    def on_up(self):
        print("up")

    def on_down(self):
        print("down")

    def on_left(self):
        print("left")

    def on_right(self):
        print("right")

    def on_knob_ctrl_volume(self):
        print("knob ctrl volume")

    def on_knob_ctrl_pan(self):
        print("knob ctrl pan")

    def on_knob_ctrl_send(self):
        print("knob ctrl send")

    def on_knob_ctrl_device(self):
        print("knob ctrl device")

    def on_stop_all_clips(self):
        print("stop all clips")

    def on_soft_key_clip_stop(self):
        print("soft key clip stop")

    def on_soft_key_solo(self):
        print("soft key solo")

    def on_soft_key_mute(self):
        print("soft key mute")

    def on_soft_key_rec_arm(self):
        print("soft key rec arm")

    def on_soft_key_select(self):
        print("soft key select")

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
