# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import mido

from ..controller import DeviceController


# NOTE: these constants are taken from:
# https://github.com/tsmetana/mpk3-settings/blob/master/src/message.h

# Offsets from the beginning of the SYSEX message
OFF_PGM_NAME                = 7

# Message constants
MANUFACTURER_ID             = 0x47
PRODUCT_ID                  = 0x49
DATA_MSG_LEN                = 252
MSG_PAYLOAD_LEN             = 246

# Message direction
MSG_DIRECTION_OUT           = 0x7f
MSG_DIRECTION_IN            = 0x00

# Command values
CMD_WRITE_DATA              = 0x64
CMD_QUERY_DATA              = 0x66
CMD_INCOMING_DATA           = 0x67

# Name (program, knob) string length
NAME_STR_LEN                = 16

# Aftertouch settings
AFTERTOUCH_OFF              = 0x00
AFTERTOUCH_CHANNEL          = 0x01
AFTERTOUCH_POLYPHONIC       = 0x02

# Keybed octave
KEY_OCTAVE_MIN              = 0x00
KEY_OCTAVE_MAX              = 0x07

# Arpeggiator settings
ARP_ON                      = 0x7f
ARP_OFF                     = 0x00
ARP_OCTAVE_MIN              = 0x00
ARP_OCTAVE_MAX              = 0x03
ARP_MODE_UP                 = 0x00
ARP_MODE_DOWN               = 0x01
ARP_MODE_EXCL               = 0x02
ARP_MODE_INCL               = 0x03
ARP_MODE_ORDER              = 0x04
ARP_MODE_RAND               = 0x05
ARP_DIV_1_4                 = 0x00
ARP_DIV_1_4T                = 0x01
ARP_DIV_1_8                 = 0x02
ARP_DIV_1_8T                = 0x03
ARP_DIV_1_16                = 0x04
ARP_DIV_1_16T               = 0x05
ARP_DIV_1_32                = 0x06
ARP_DIV_1_32T               = 0x07
ARP_LATCH_OFF               = 0x00
ARP_LATCH_ON                = 0x01
ARP_SWING_MIN               = 0x00
ARP_SWING_MAX               = 0x19

# Clock settings
CLK_INTERNAL                = 0x00
CLK_EXTERNAL                = 0x01
TEMPO_TAPS_MIN              = 2
TEMPO_TAPS_MAX              = 4
BPM_MIN                     = 60
BPM_MAX                     = 240

# Joystick
JOY_MODE_PITCHBEND          = 0x00
JOY_MODE_SINGLE             = 0x01
JOY_MODE_DUAL               = 0x02

# Knobs
KNOB_MODE_ABS               = 0
KNOB_MODE_REL               = 1


class SysExQueryProgram:
    def __init__(self, program=0):
        assert 0 <= program <= 8, "Invalid program number, only 0 (RAM) to 8 available."

        self.data = [
            MANUFACTURER_ID, MSG_DIRECTION_OUT, PRODUCT_ID, CMD_QUERY_DATA,
            0, 1, program,
        ]

    def __iter__(self):
        return iter(self.data)


class SysExSetProgram:
    def __init__(self, program=0, name="MDevTK", channels={}, aftertouch=AFTERTOUCH_OFF,
                 keybed_octave=4, arp={}, ext_clock=False, tempo_taps=3, tempo=60, joy={},
                 pads={}, knobs={}, transpose=0x0c):
        arp_swing = int(arp.get("swing", ARP_SWING_MIN))

        assert 0 <= program <= 8, "Invalid program number: {program} (valid: 0(RAM)-8)."
        assert aftertouch in [AFTERTOUCH_OFF, AFTERTOUCH_CHANNEL, AFTERTOUCH_POLYPHONIC], \
            f"Invalid aftertouch mode: {aftertouch} (valid: 0-2)."
        assert KEY_OCTAVE_MIN <= keybed_octave <= KEY_OCTAVE_MAX, \
            f"Invalid keybed octave: {keybed_octave} (valid: 0-8)."
        assert ARP_SWING_MIN <= arp_swing <= ARP_SWING_MAX, \
            f"Invalid swing value: {arp_swing} (valid: 0-25)."
        assert TEMPO_TAPS_MIN <= tempo_taps <= TEMPO_TAPS_MAX, \
            f"Invalid tempo taps: {tempo_taps} (valid: {TEMPO_TAPS_MIN}-{TEMPO_TAPS_MAX})."
        assert BPM_MIN <= tempo <= BPM_MAX, f"Invalid tempo: {tempo} (valid: 60-240)."
        for c in channels.values():
            assert 0 <= c <= 15, f"Invalid channel number: {c} (valid: 0-15)."
        for field in ["note", "pc", "cc"]:
            assert field in pads, f"Invalid pads definition, missing '{field}' list."
            assert len(pads[field]) == 16, f"Invalid pads definition, len('{field}') != 16."
            for v in pads[field]:
                assert 0 <= v <= 127, f"Invalid pads definition, invalid value: {v}."
        for field in ["mode", "cc", "min", "max", "name"]:
            assert field in knobs, f"Invalid knobs definition, missing '{field}' list."
            assert len(knobs[field]) == 8, f"Invalid knobs definition, len('{field}') != 8."

        self.data = [
            MANUFACTURER_ID, MSG_DIRECTION_OUT, PRODUCT_ID, CMD_WRITE_DATA,
            (MSG_PAYLOAD_LEN >> 7) & 127, MSG_PAYLOAD_LEN & 127, program,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            channels.get("pad", 9),
            aftertouch,
            channels.get("keybed", 0),
            keybed_octave,
            ARP_ON if arp.get("on") else ARP_OFF,
            arp.get("mode", ARP_MODE_UP),
            arp.get("division", ARP_DIV_1_4),
            CLK_EXTERNAL if ext_clock else CLK_INTERNAL,
            ARP_LATCH_ON if arp.get("latch", False) else ARP_LATCH_OFF,
            arp_swing,
            tempo_taps, (tempo >> 7) & 127, tempo & 127,
            arp.get("octave", ARP_OCTAVE_MIN),
            joy.get("x-mode", JOY_MODE_PITCHBEND), joy.get("x-neg-ch", 1), joy.get("x-pos-ch", 2),
            joy.get("y-mode", JOY_MODE_DUAL), joy.get("y-neg-ch", 1), joy.get("y-pos-ch", 2),
        ]

        for pidx in range(16):
            self.data.append(pads["note"][pidx])
            self.data.append(pads["pc"][pidx])
            self.data.append(pads["cc"][pidx])

        for kidx in range(8):
            self.data.append(knobs["mode"][kidx])
            self.data.append(knobs["cc"][kidx])
            self.data.append(knobs["min"][kidx])
            self.data.append(knobs["max"][kidx])
            padname = list(bytes(16))
            padname[:len(knobs["name"][kidx])] = [ord(c) for c in knobs["name"][kidx]]
            self.data += padname

        self.data.append(transpose)

        padname = list(bytes(16))
        padname[:len(name)] = [ord(c) for c in name]
        self.data[OFF_PGM_NAME:OFF_PGM_NAME + NAME_STR_LEN] = padname[:NAME_STR_LEN]

        assert len(self.data) == DATA_MSG_LEN, \
            f"ERROR, invalid message size!! ({len(self.data)} != {DATA_MSG_LEN})"

    def __iter__(self):
        return iter(self.data)


class MPKMiniMK3(DeviceController):
    def __init__(self):
        super().__init__("MPK mini 3")
        self._setup_device()

        self.on_note(channel=9, note=36, cb="on_pad_1", bank="A")
        self.on_note(channel=9, note=37, cb="on_pad_2", bank="A")
        self.on_note(channel=9, note=38, cb="on_pad_3", bank="A")
        self.on_note(channel=9, note=39, cb="on_pad_4", bank="A")
        self.on_note(channel=9, note=40, cb="on_pad_5", bank="A")
        self.on_note(channel=9, note=41, cb="on_pad_6", bank="A")
        self.on_note(channel=9, note=42, cb="on_pad_7", bank="A")
        self.on_note(channel=9, note=43, cb="on_pad_8", bank="A")

        self.on_note(channel=9, note=44, cb="on_pad_1", bank="B")
        self.on_note(channel=9, note=45, cb="on_pad_2", bank="B")
        self.on_note(channel=9, note=46, cb="on_pad_3", bank="B")
        self.on_note(channel=9, note=47, cb="on_pad_4", bank="B")
        self.on_note(channel=9, note=48, cb="on_pad_5", bank="B")
        self.on_note(channel=9, note=49, cb="on_pad_6", bank="B")
        self.on_note(channel=9, note=50, cb="on_pad_7", bank="B")
        self.on_note(channel=9, note=51, cb="on_pad_8", bank="B")

        self.on_polytouch(channel=9, note=36, cb="on_pad_1_at", bank="A")
        self.on_polytouch(channel=9, note=37, cb="on_pad_2_at", bank="A")
        self.on_polytouch(channel=9, note=38, cb="on_pad_3_at", bank="A")
        self.on_polytouch(channel=9, note=39, cb="on_pad_4_at", bank="A")
        self.on_polytouch(channel=9, note=40, cb="on_pad_5_at", bank="A")
        self.on_polytouch(channel=9, note=41, cb="on_pad_6_at", bank="A")
        self.on_polytouch(channel=9, note=42, cb="on_pad_7_at", bank="A")
        self.on_polytouch(channel=9, note=43, cb="on_pad_8_at", bank="A")

        self.on_polytouch(channel=9, note=44, cb="on_pad_1_at", bank="B")
        self.on_polytouch(channel=9, note=45, cb="on_pad_2_at", bank="B")
        self.on_polytouch(channel=9, note=46, cb="on_pad_3_at", bank="B")
        self.on_polytouch(channel=9, note=47, cb="on_pad_4_at", bank="B")
        self.on_polytouch(channel=9, note=48, cb="on_pad_5_at", bank="B")
        self.on_polytouch(channel=9, note=49, cb="on_pad_6_at", bank="B")
        self.on_polytouch(channel=9, note=50, cb="on_pad_7_at", bank="B")
        self.on_polytouch(channel=9, note=51, cb="on_pad_8_at", bank="B")

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

        self.on_cc(channel=0, controls=(1,), cb="on_y_axis", direction="up")
        self.on_cc(channel=0, controls=(2,), cb="on_y_axis", direction="down")
        self.on_pitchwheel(channel=0, cb="on_x_axis")

    def _setup_device(self):
        cmd = SysExSetProgram(
            pads = {
                "note": range(36, 52),
                "pc": range(16),
                "cc": range(16, 32),
            },
            knobs = {
                "mode": [KNOB_MODE_ABS for _ in range(8)],
                "cc": range(70, 78),
                "min": [0 for _ in range(8)],
                "max": [127 for _ in range(8)],
                "name": [f"MyKNOB-{i}" for i in range(8)],
            }
        )
        msg = mido.Message(type="sysex", data=cmd)
        self._port.send(msg)

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

    def on_pad_at(self, pad_number, value, bank):
        pass

    def on_pad_1_at(self, value, bank):
        self.on_pad_at(1, value, bank)

    def on_pad_2_at(self, value, bank):
        self.on_pad_at(2, value, bank)

    def on_pad_3_at(self, value, bank):
        self.on_pad_at(3, value, bank)

    def on_pad_4_at(self, value, bank):
        self.on_pad_at(4, value, bank)

    def on_pad_5_at(self, value, bank):
        self.on_pad_at(5, value, bank)

    def on_pad_6_at(self, value, bank):
        self.on_pad_at(6, value, bank)

    def on_pad_7_at(self, value, bank):
        self.on_pad_at(7, value, bank)

    def on_pad_8_at(self, value, bank):
        self.on_pad_at(8, value, bank)
