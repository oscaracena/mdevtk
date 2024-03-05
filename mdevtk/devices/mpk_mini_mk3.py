# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from ..controller import DeviceController


class MPKMiniMK3(DeviceController):
    # NOTE: This mapping uses the factory PROGRAM called 'MPC'. Other programs
    # may (and probably would) change this mapping!

    def __init__(self):
        super().__init__("MPK mini 3")

        self.on_note(channel=9, note=36,  cb="on_pad_1", bank="A")
        self.on_note(channel=9, note=37,  cb="on_pad_2", bank="A")
        self.on_note(channel=9, note=38,  cb="on_pad_3", bank="A")
        self.on_note(channel=9, note=39,  cb="on_pad_4", bank="A")
        self.on_note(channel=9, note=40,  cb="on_pad_5", bank="A")
        self.on_note(channel=9, note=41,  cb="on_pad_6", bank="A")
        self.on_note(channel=9, note=42,  cb="on_pad_7", bank="A")
        self.on_note(channel=9, note=43,  cb="on_pad_8", bank="A")

        self.on_note(channel=9, note=44,  cb="on_pad_1", bank="B")
        self.on_note(channel=9, note=45,  cb="on_pad_2", bank="B")
        self.on_note(channel=9, note=46,  cb="on_pad_3", bank="B")
        self.on_note(channel=9, note=47,  cb="on_pad_4", bank="B")
        self.on_note(channel=9, note=48,  cb="on_pad_5", bank="B")
        self.on_note(channel=9, note=49,  cb="on_pad_6", bank="B")
        self.on_note(channel=9, note=50,  cb="on_pad_7", bank="B")
        self.on_note(channel=9, note=51,  cb="on_pad_8", bank="B")

        self.on_cc(channel=9, controls=(16,), cb="on_pad_1_cc", bank="A")
        self.on_cc(channel=9, controls=(17,), cb="on_pad_2_cc", bank="A")
        self.on_cc(channel=9, controls=(18,), cb="on_pad_3_cc", bank="A")
        self.on_cc(channel=9, controls=(19,), cb="on_pad_4_cc", bank="A")
        self.on_cc(channel=9, controls=(20,), cb="on_pad_5_cc", bank="A")
        self.on_cc(channel=9, controls=(21,), cb="on_pad_6_cc", bank="A")
        self.on_cc(channel=9, controls=(22,), cb="on_pad_7_cc", bank="A")
        self.on_cc(channel=9, controls=(23,), cb="on_pad_8_cc", bank="A")

        self.on_cc(channel=9, controls=(24,), cb="on_pad_1_cc", bank="B")
        self.on_cc(channel=9, controls=(25,), cb="on_pad_2_cc", bank="B")
        self.on_cc(channel=9, controls=(26,), cb="on_pad_3_cc", bank="B")
        self.on_cc(channel=9, controls=(27,), cb="on_pad_4_cc", bank="B")
        self.on_cc(channel=9, controls=(28,), cb="on_pad_5_cc", bank="B")
        self.on_cc(channel=9, controls=(29,), cb="on_pad_6_cc", bank="B")
        self.on_cc(channel=9, controls=(30,), cb="on_pad_7_cc", bank="B")
        self.on_cc(channel=9, controls=(31,), cb="on_pad_8_cc", bank="B")

        self.on_cc(channel=0, controls=(70,), cb="on_knob_1")
        self.on_cc(channel=0, controls=(71,), cb="on_knob_2")
        self.on_cc(channel=0, controls=(72,), cb="on_knob_3")
        self.on_cc(channel=0, controls=(73,), cb="on_knob_4")
        self.on_cc(channel=0, controls=(74,), cb="on_knob_5")
        self.on_cc(channel=0, controls=(75,), cb="on_knob_6")
        self.on_cc(channel=0, controls=(76,), cb="on_knob_7")
        self.on_cc(channel=0, controls=(77,), cb="on_knob_8")

        self.on_cc(channel=0, controls=(1,), cb="on_y_axis")

        self.on_pc(channel=9, program=0, cb="on_pad_1_pc", bank="A")
        self.on_pc(channel=9, program=1, cb="on_pad_2_pc", bank="A")
        self.on_pc(channel=9, program=2, cb="on_pad_3_pc", bank="A")
        self.on_pc(channel=9, program=3, cb="on_pad_4_pc", bank="A")
        self.on_pc(channel=9, program=4, cb="on_pad_5_pc", bank="A")
        self.on_pc(channel=9, program=5, cb="on_pad_6_pc", bank="A")
        self.on_pc(channel=9, program=6, cb="on_pad_7_pc", bank="A")
        self.on_pc(channel=9, program=7, cb="on_pad_8_pc", bank="A")

        self.on_pc(channel=9, program=8, cb="on_pad_1_pc", bank="B")
        self.on_pc(channel=9, program=9, cb="on_pad_2_pc", bank="B")
        self.on_pc(channel=9, program=10, cb="on_pad_3_pc", bank="B")
        self.on_pc(channel=9, program=11, cb="on_pad_4_pc", bank="B")
        self.on_pc(channel=9, program=12, cb="on_pad_5_pc", bank="B")
        self.on_pc(channel=9, program=13, cb="on_pad_6_pc", bank="B")
        self.on_pc(channel=9, program=14, cb="on_pad_7_pc", bank="B")
        self.on_pc(channel=9, program=15, cb="on_pad_8_pc", bank="B")

        self.on_aftertouch(channel=9, cb="on_pad_aftertouch")
        self.on_pitchwheel(channel=0, cb="on_x_axis")

    def on_pad_pressed(self, pad_number, bank):
        pass

    def on_pad_1(self, bank):
        self.on_pad_pressed(1, bank)

    def on_pad_2(self, bank):
        self.on_pad_pressed(2, bank)

    def on_pad_3(self, bank):
        self.on_pad_pressed(3, bank)

    def on_pad_4(self, bank):
        self.on_pad_pressed(4, bank)

    def on_pad_5(self, bank):
        self.on_pad_pressed(5, bank)

    def on_pad_6(self, bank):
        self.on_pad_pressed(6, bank)

    def on_pad_7(self, bank):
        self.on_pad_pressed(7, bank)

    def on_pad_8(self, bank):
        self.on_pad_pressed(8, bank)

    def on_pad_cc(self, pad_number, value, bank):
        pass

    def on_pad_1_cc(self, value, bank):
        self.on_pad_cc(1, value, bank)

    def on_pad_2_cc(self, value, bank):
        self.on_pad_cc(2, value, bank)

    def on_pad_3_cc(self, value, bank):
        self.on_pad_cc(3, value, bank)

    def on_pad_4_cc(self, value, bank):
        self.on_pad_cc(4, value, bank)

    def on_pad_5_cc(self, value, bank):
        self.on_pad_cc(5, value, bank)

    def on_pad_6_cc(self, value, bank):
        self.on_pad_cc(6, value, bank)

    def on_pad_7_cc(self, value, bank):
        self.on_pad_cc(7, value, bank)

    def on_pad_8_cc(self, value, bank):
        self.on_pad_cc(8, value, bank)

    def on_pad_pc(self, pad_number, program, bank):
        pass

    def on_pad_1_pc(self, program, bank):
        self.on_pad_pc(1, program, bank)

    def on_pad_2_pc(self, program, bank):
        self.on_pad_pc(2, program, bank)

    def on_pad_3_pc(self, program, bank):
        self.on_pad_pc(3, program, bank)

    def on_pad_4_pc(self, program, bank):
        self.on_pad_pc(4, program, bank)

    def on_pad_5_pc(self, program, bank):
        self.on_pad_pc(5, program, bank)

    def on_pad_6_pc(self, program, bank):
        self.on_pad_pc(6, program, bank)

    def on_pad_7_pc(self, program, bank):
        self.on_pad_pc(7, program, bank)

    def on_pad_8_pc(self, program, bank):
        self.on_pad_pc(8, program, bank)
