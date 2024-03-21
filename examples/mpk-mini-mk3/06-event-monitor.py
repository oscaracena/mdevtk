#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from mdevtk import MPKMiniMK3


class MyMPKMiniMK3(MPKMiniMK3):
    # NOTE: instead of overriding 'on_pad_N()', you can use 'on_pad_pressed(n)'
    def on_pad_pressed(self, number, bank):
        print(f"pad number: {number}, bank: {bank}")

    # def on_pad_1(self, bank):
    #     print(f"pad 1, bank {bank}")

    # def on_pad_2(self, bank):
    #     print(f"pad 2, bank {bank}")

    def on_pad_3(self, bank):
        print(f"pad 3, bank {bank}")

    def on_pad_4(self, bank):
        print(f"pad 4, bank {bank}")

    def on_pad_5(self, bank):
        print(f"pad 5, bank {bank}")

    def on_pad_6(self, bank):
        print(f"pad 6, bank {bank}")

    def on_pad_7(self, bank):
        print(f"pad 7, bank {bank}")

    def on_pad_8(self, bank):
        print(f"pad 8, bank {bank}")

    # NOTE: instead of overriding 'on_pad_N_cc()', you can use 'on_pad_cc(n)'
    def on_pad_cc(self, number, value, bank):
        print(f"pad CC number: {number}, value: {value}, bank: {bank}")

    # def on_pad_1_cc(self, value, bank):
    #     print(f"pad 1 CC, value: {value}, bank {bank}")

    # def on_pad_2_cc(self, value, bank):
    #     print(f"pad 2 CC, value: {value}, bank {bank}")

    def on_pad_3_cc(self, value, bank):
        print(f"pad 3 CC, value: {value}, bank {bank}")

    def on_pad_4_cc(self, value, bank):
        print(f"pad 4 CC, value: {value}, bank {bank}")

    def on_pad_5_cc(self, value, bank):
        print(f"pad 5 CC, value: {value}, bank {bank}")

    def on_pad_6_cc(self, value, bank):
        print(f"pad 6 CC, value: {value}, bank {bank}")

    def on_pad_7_cc(self, value, bank):
        print(f"pad 7 CC, value: {value}, bank {bank}")

    def on_pad_8_cc(self, value, bank):
        print(f"pad 8 CC, value: {value}, bank {bank}")

    # NOTE: instead of overriding 'on_pad_N_pc()', you can use 'on_pad_pc(n)'
    def on_pad_pc(self, number, program, bank):
        print(f"pad PC number: {number}, program: {program}, bank: {bank}")

    # def on_pad_1_pc(self, program, bank):
    #     print(f"pad 1 PC, program: {program}, bank {bank}")

    # def on_pad_2_pc(self, program, bank):
    #     print(f"pad 2 PC, program: {program}, bank {bank}")

    def on_pad_3_pc(self, program, bank):
        print(f"pad 3 PC, program: {program}, bank {bank}")

    def on_pad_4_pc(self, program, bank):
        print(f"pad 4 PC, program: {program}, bank {bank}")

    def on_pad_5_pc(self, program, bank):
        print(f"pad 5 PC, program: {program}, bank {bank}")

    def on_pad_6_pc(self, program, bank):
        print(f"pad 6 PC, program: {program}, bank {bank}")

    def on_pad_7_pc(self, program, bank):
        print(f"pad 7 PC, program: {program}, bank {bank}")

    def on_pad_8_pc(self, program, bank):
        print(f"pad 8 PC, program: {program}, bank {bank}")

    # NOTE: instead of overriding 'on_pad_N_at()', you can use 'on_pad_at(n)'
    def on_pad_at(self, number, value, bank):
        print(f"pad AfterTouch number: {number}, value: {value}, bank: {bank}")

    # def on_pad_1_at(self, value, bank):
    #     print(f"pad 1 AfterTouch, value: {value}, bank {bank}")

    # def on_pad_2_at(self, value, bank):
    #     print(f"pad 2 AfterTouch, value: {value}, bank {bank}")

    def on_pad_3_at(self, value, bank):
        print(f"pad 3 AfterTouch, value: {value}, bank {bank}")

    def on_pad_4_at(self, value, bank):
        print(f"pad 4 AfterTouch, value: {value}, bank {bank}")

    def on_pad_5_at(self, value, bank):
        print(f"pad 5 AfterTouch, value: {value}, bank {bank}")

    def on_pad_6_at(self, value, bank):
        print(f"pad 6 AfterTouch, value: {value}, bank {bank}")

    def on_pad_7_at(self, value, bank):
        print(f"pad 7 AfterTouch, value: {value}, bank {bank}")

    def on_pad_8_at(self, value, bank):
        print(f"pad 8 AfterTouch, value: {value}, bank {bank}")

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

    def on_x_axis(self, value):
        print(f"joystick x axis, value: {value}")

    def on_y_axis(self, value, direction):
        print(f"joystick y axis, value: {value}, direction: {direction}")


try:
    device = MyMPKMiniMK3()
    print("Press/rotate any pad, key or knob...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")
