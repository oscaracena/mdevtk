# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import mido
from ..controller import DeviceController


class APCKey25MK2(DeviceController):
    # valid color combinations (velocity = color index in list)
    COLORS = [
        0x000000, 0x1E1E1E, 0x7F7F7F, 0xFFFFFF, 0xFF4C4C, 0xFF0000, 0x590000,
        0x190000, 0xFFBD6C, 0xFF5400, 0x591D00, 0x271B00, 0xFFFF4C, 0xFFFF00,
        0x595900, 0x191900, 0x88FF4C, 0x54FF00, 0x1D5900, 0x142B00, 0x4CFF4C,
        0x00FF00, 0x005900, 0x001900, 0x4CFF5E, 0x00FF19, 0x00590D, 0x001902,
        0x4CFF88, 0x00FF55, 0x00591D, 0x001F12, 0x4CFFB7, 0x00FF99, 0x005935,
        0x001912, 0x4CC3FF, 0x00A9FF, 0x004152, 0x001019, 0x4C88FF, 0x0055FF,
        0x001D59, 0x000819, 0x4C4CFF, 0x0000FF, 0x000059, 0x000019, 0x874CFF,
        0x5400FF, 0x190064, 0x0F0030, 0xFF4CFF, 0xFF00FF, 0x590059, 0x190019,
        0xFF4C87, 0xFF0054, 0x59001D, 0x220013, 0xFF1500, 0x993500, 0x795100,
        0x436400, 0x033900, 0x005735, 0x00547F, 0x0000FF, 0x00454F, 0x2500CC,
        0x7F7F7F, 0x202020, 0xFF0000, 0xBDFF2D, 0xAFED06, 0x64FF09, 0x108B00,
        0x00FF87, 0x00A9FF, 0x002AFF, 0x3F00FF, 0x7A00FF, 0xB21A7D, 0x402100,
        0xFF4A00, 0x88E106, 0x72FF15, 0x00FF00, 0x3BFF26, 0x59FF71, 0x38FFCC,
        0x5B8AFF, 0x3151C6, 0x877FE9, 0xD31DFF, 0xFF005D, 0xFF7F00, 0xB9B000,
        0x90FF00, 0x835D07, 0x392b00, 0x144C10, 0x0D5038, 0x15152A, 0x16205A,
        0x693C1C, 0xA8000A, 0xDE513D, 0xD86A1C, 0xFFE126, 0x9EE12F, 0x67B50F,
        0x1E1E30, 0xDCFF6B, 0x80FFBD, 0x9A99FF, 0x8E66FF, 0x404040, 0x757575,
        0xE0FFFF, 0xA00000, 0x350000, 0x1AD000, 0x074200, 0xB9B000, 0x3F3100,
        0xB35F00, 0x4B1502, 0x404040, 0x757575, 0xE0FFFF, 0xA00000, 0x350000,
        0x1AD000, 0x074200, 0xB9B000, 0x3F3100, 0xB35F00, 0x4B1502,
    ]

    LED_BRIGHT_10   = 0
    LED_BRIGHT_25   = 1
    LED_BRIGHT_50   = 2
    LED_BRIGHT_65   = 3
    LED_BRIGHT_75   = 4
    LED_BRIGHT_90   = 5
    LED_BRIGHT_100  = 6

    LED_PULSING_16  = 7
    LED_PULSING_8   = 8
    LED_PULSING_4   = 9
    LED_PULSING_2   = 10

    LED_BLINKING_24 = 11
    LED_BLINKING_16 = 12
    LED_BLINKING_8  = 13
    LED_BLINKING_4  = 14
    LED_BLINKING_2  = 15

    # LED ids: (channel, note)
    TRACK_1         = (0, 0x40)
    TRACK_2         = (0, 0x41)
    TRACK_3         = (0, 0x42)
    TRACK_4         = (0, 0x43)
    TRACK_5         = (0, 0x44)
    TRACK_6         = (0, 0x45)
    TRACK_7         = (0, 0x46)
    TRACK_8         = (0, 0x47)

    SCENE_1         = (0, 0x52)
    SCENE_2         = (0, 0x53)
    SCENE_3         = (0, 0x54)
    SCENE_4         = (0, 0x55)
    SCENE_5         = (0, 0x56)

    # PAD buttons: (channel, note)
    PAD_1           = (6, 0x00)
    PAD_2           = (6, 0x01)
    PAD_3           = (6, 0x02)
    PAD_4           = (6, 0x03)
    PAD_5           = (6, 0x04)
    PAD_6           = (6, 0x05)
    PAD_7           = (6, 0x06)
    PAD_8           = (6, 0x07)
    PAD_9           = (6, 0x08)
    PAD_10          = (6, 0x09)
    PAD_11          = (6, 0x0a)
    PAD_12          = (6, 0x0b)
    PAD_13          = (6, 0x0c)
    PAD_14          = (6, 0x0d)
    PAD_15          = (6, 0x0e)
    PAD_16          = (6, 0x0f)
    PAD_17          = (6, 0x10)
    PAD_18          = (6, 0x11)
    PAD_19          = (6, 0x12)
    PAD_20          = (6, 0x13)
    PAD_21          = (6, 0x14)
    PAD_22          = (6, 0x15)
    PAD_23          = (6, 0x16)
    PAD_24          = (6, 0x17)
    PAD_25          = (6, 0x18)
    PAD_26          = (6, 0x19)
    PAD_27          = (6, 0x1a)
    PAD_28          = (6, 0x1b)
    PAD_29          = (6, 0x1c)
    PAD_30          = (6, 0x1d)
    PAD_31          = (6, 0x1e)
    PAD_32          = (6, 0x1f)
    PAD_33          = (6, 0x20)
    PAD_34          = (6, 0x21)
    PAD_35          = (6, 0x22)
    PAD_36          = (6, 0x23)
    PAD_37          = (6, 0x24)
    PAD_38          = (6, 0x25)
    PAD_39          = (6, 0x26)
    PAD_40          = (6, 0x27)

    # some LED aliases
    LED_UP          = TRACK_1
    LED_LED_DOWN    = TRACK_2
    LED_LEFT        = TRACK_3
    LED_RIGHT       = TRACK_4
    LED_VOLUME      = TRACK_5
    LED_PAN         = TRACK_6
    LED_SEND        = TRACK_7
    LED_DEVICE      = TRACK_8

    LED_CLIP_STOP   = SCENE_1
    LED_SOLO        = SCENE_2
    LED_MUTE        = SCENE_3
    LED_REC_ARM     = SCENE_4
    LED_SELECT      = SCENE_5

    # FIXME: add callback aliases for TRACK_ and SECENE_ buttons
    # FIXME: add support for port 0 (keybed and sustain button)
    # FIXME: add support for note-off events too

    def __init__(self):
        # NOTE: C = port 1, K = port 0
        super().__init__("APC Key 25 mk2 C")

        self.on_note(channel=0, note=0,  cb="on_pad_1")
        self.on_note(channel=0, note=1,  cb="on_pad_2")
        self.on_note(channel=0, note=2,  cb="on_pad_3")
        self.on_note(channel=0, note=3,  cb="on_pad_4")
        self.on_note(channel=0, note=4,  cb="on_pad_5")
        self.on_note(channel=0, note=5,  cb="on_pad_6")
        self.on_note(channel=0, note=6,  cb="on_pad_7")
        self.on_note(channel=0, note=7,  cb="on_pad_8")
        self.on_note(channel=0, note=8,  cb="on_pad_9")
        self.on_note(channel=0, note=9,  cb="on_pad_10")
        self.on_note(channel=0, note=10, cb="on_pad_11")
        self.on_note(channel=0, note=11, cb="on_pad_12")
        self.on_note(channel=0, note=12, cb="on_pad_13")
        self.on_note(channel=0, note=13, cb="on_pad_14")
        self.on_note(channel=0, note=14, cb="on_pad_15")
        self.on_note(channel=0, note=15, cb="on_pad_16")
        self.on_note(channel=0, note=16, cb="on_pad_17")
        self.on_note(channel=0, note=17, cb="on_pad_18")
        self.on_note(channel=0, note=18, cb="on_pad_19")
        self.on_note(channel=0, note=19, cb="on_pad_20")
        self.on_note(channel=0, note=20, cb="on_pad_21")
        self.on_note(channel=0, note=21, cb="on_pad_22")
        self.on_note(channel=0, note=22, cb="on_pad_23")
        self.on_note(channel=0, note=23, cb="on_pad_24")
        self.on_note(channel=0, note=24, cb="on_pad_25")
        self.on_note(channel=0, note=25, cb="on_pad_26")
        self.on_note(channel=0, note=26, cb="on_pad_27")
        self.on_note(channel=0, note=27, cb="on_pad_28")
        self.on_note(channel=0, note=28, cb="on_pad_29")
        self.on_note(channel=0, note=29, cb="on_pad_30")
        self.on_note(channel=0, note=30, cb="on_pad_31")
        self.on_note(channel=0, note=31, cb="on_pad_32")
        self.on_note(channel=0, note=32, cb="on_pad_33")
        self.on_note(channel=0, note=33, cb="on_pad_34")
        self.on_note(channel=0, note=34, cb="on_pad_35")
        self.on_note(channel=0, note=35, cb="on_pad_36")
        self.on_note(channel=0, note=36, cb="on_pad_37")
        self.on_note(channel=0, note=37, cb="on_pad_38")
        self.on_note(channel=0, note=38, cb="on_pad_39")
        self.on_note(channel=0, note=39, cb="on_pad_40")

        self.on_note(channel=0, note=64, cb="on_up")
        self.on_note(channel=0, note=65, cb="on_down")
        self.on_note(channel=0, note=66, cb="on_left")
        self.on_note(channel=0, note=67, cb="on_right")
        self.on_note(channel=0, note=68, cb="on_knob_ctrl_volume")
        self.on_note(channel=0, note=69, cb="on_knob_ctrl_pan")
        self.on_note(channel=0, note=70, cb="on_knob_ctrl_send")
        self.on_note(channel=0, note=71, cb="on_knob_ctrl_device")
        self.on_note(channel=0, note=81, cb="on_stop_all_clips")
        self.on_note(channel=0, note=82, cb="on_soft_key_clip_stop")
        self.on_note(channel=0, note=83, cb="on_soft_key_solo")
        self.on_note(channel=0, note=84, cb="on_soft_key_mute")
        self.on_note(channel=0, note=85, cb="on_soft_key_rec_arm")
        self.on_note(channel=0, note=86, cb="on_soft_key_select")
        self.on_note(channel=0, note=91, cb="on_play")
        self.on_note(channel=0, note=93, cb="on_rec")
        self.on_note(channel=0, note=98, cb="on_shift")

        self.on_cc(channel=0, controls=(48,), cb="on_knob_1")
        self.on_cc(channel=0, controls=(49,), cb="on_knob_2")
        self.on_cc(channel=0, controls=(50,), cb="on_knob_3")
        self.on_cc(channel=0, controls=(51,), cb="on_knob_4")
        self.on_cc(channel=0, controls=(52,), cb="on_knob_5")
        self.on_cc(channel=0, controls=(53,), cb="on_knob_6")
        self.on_cc(channel=0, controls=(54,), cb="on_knob_7")
        self.on_cc(channel=0, controls=(55,), cb="on_knob_8")

    def on_pad_pressed(self, pad_number):
        pass

    def on_pad_1(self):
        self.on_pad_pressed(1)

    def on_pad_2(self):
        self.on_pad_pressed(2)

    def on_pad_3(self):
        self.on_pad_pressed(3)

    def on_pad_4(self):
        self.on_pad_pressed(4)

    def on_pad_5(self):
        self.on_pad_pressed(5)

    def on_pad_6(self):
        self.on_pad_pressed(6)

    def on_pad_7(self):
        self.on_pad_pressed(7)

    def on_pad_8(self):
        self.on_pad_pressed(8)

    def on_pad_9(self):
        self.on_pad_pressed(9)

    def on_pad_10(self):
        self.on_pad_pressed(10)

    def on_pad_11(self):
        self.on_pad_pressed(11)

    def on_pad_12(self):
        self.on_pad_pressed(12)

    def on_pad_13(self):
        self.on_pad_pressed(13)

    def on_pad_14(self):
        self.on_pad_pressed(14)

    def on_pad_15(self):
        self.on_pad_pressed(15)

    def on_pad_16(self):
        self.on_pad_pressed(16)

    def on_pad_17(self):
        self.on_pad_pressed(17)

    def on_pad_18(self):
        self.on_pad_pressed(18)

    def on_pad_19(self):
        self.on_pad_pressed(19)

    def on_pad_20(self):
        self.on_pad_pressed(20)

    def on_pad_21(self):
        self.on_pad_pressed(21)

    def on_pad_22(self):
        self.on_pad_pressed(22)

    def on_pad_23(self):
        self.on_pad_pressed(23)

    def on_pad_24(self):
        self.on_pad_pressed(24)

    def on_pad_25(self):
        self.on_pad_pressed(25)

    def on_pad_26(self):
        self.on_pad_pressed(26)

    def on_pad_27(self):
        self.on_pad_pressed(27)

    def on_pad_28(self):
        self.on_pad_pressed(28)

    def on_pad_29(self):
        self.on_pad_pressed(29)

    def on_pad_30(self):
        self.on_pad_pressed(30)

    def on_pad_31(self):
        self.on_pad_pressed(31)

    def on_pad_32(self):
        self.on_pad_pressed(32)

    def on_pad_33(self):
        self.on_pad_pressed(33)

    def on_pad_34(self):
        self.on_pad_pressed(34)

    def on_pad_35(self):
        self.on_pad_pressed(35)

    def on_pad_36(self):
        self.on_pad_pressed(36)

    def on_pad_37(self):
        self.on_pad_pressed(37)

    def on_pad_38(self):
        self.on_pad_pressed(38)

    def on_pad_39(self):
        self.on_pad_pressed(39)

    def on_pad_40(self):
        self.on_pad_pressed(40)

    def on_track_change(self, track_number):
        pass

    def on_up(self):
        self.on_track_change(1)

    def on_down(self):
        self.on_track_change(2)

    def on_left(self):
        self.on_track_change(3)

    def on_right(self):
        self.on_track_change(4)

    def on_knob_ctrl_volume(self):
        self.on_track_change(5)

    def on_knob_ctrl_pan(self):
        self.on_track_change(6)

    def on_knob_ctrl_send(self):
        self.on_track_change(7)

    def on_knob_ctrl_device(self):
        self.on_track_change(8)

    def set_pad_led(self, pad, color, mode):
        msg = mido.Message(type="note_on", channel=mode, note=pad, velocity=color)
        self._port.send(msg)

    def set_rgb_led(self, led_id, r, g, b):
        channel, note = led_id
        value = self._rgb_to_value(r, g, b)
        if value == -1:
            return

        msg = mido.Message(type="note_on", channel=channel, note=note, velocity=value)
        self._port.send(msg)
        return

    def _rgb_to_value(self, r, g, b):
        r = min(255, max(0, r))
        g = min(255, max(0, g))
        b = min(255, max(0, b))
        c = (r << 16) + (g << 8) + b

        try:
            return self.COLORS.index(c)
        except ValueError:
            return -1
