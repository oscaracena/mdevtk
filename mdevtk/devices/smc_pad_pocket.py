# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2025, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import time
from threading import Event

import mido

from ..controller import DeviceController
try:
    from hexdump import hexdump
except ImportError:
    hexdump = print


class SMCPadPocket(DeviceController):
    DEVID_CTRL            = [0x00, 0x32, 0x09]
    DEVID_STAT            = [0x00, 0x32, 0x0D]
    DEVID_ACK             = [0x00, 0x32, 0x01]

    PRESETS_0             = [0x70, 0x16]
    PRESETS_1             = [0x63, 0x2D]
    PRESETS_2             = [0x56, 0x44]
    PRESETS_3             = [0x49, 0x5B]

    PROP_LED_OFFSET       = 0x05
    PROP_NOTE_OFFSET      = 0x02
    PROP_CHANNEL_OFFSET   = 0x01
    PROP_TYPE_OFFSET      = 0x00
    PROP_MODE_OFFSET      = 2912

    def __init__(self, note_start=36, channel=9, debug=False, wait_on_send=True,
            autoconnect=True):

        super().__init__("SMC-PAD Pocket-Private")
        self._synced = Event()
        self._wait_on_send = wait_on_send
        self._debug = debug

        # public properties
        self.preset = 0
        self.bank = 0

        self.on_sysex(self.DEVID_STAT, self._recv_sysex)
        if autoconnect:
            self.connect(note_start, channel)

    def connect(self, note_start: int, channel: int, ptype="note"):
        for col in range(4):
            for row in range(4):
                pad = row * 4 + col
                note = note_start + pad
                if ptype == "momentary":
                    self.on_cc(
                        channel=channel, controls=[note], cb="on_pad",
                        pad=pad, row=row, col=col)
                elif ptype == "note":
                    self.on_note(
                        channel=channel, note=note, cb="on_pad",
                        pad=pad, row=row, col=col)
                else:
                    raise RuntimeError("Unsupported type")

    def change_bank(self, bank: int):
        # Message format:
        # - DEVID[3] 49 00 00 40 02 PRESET[2] 00 00 10 00 00 00 BANK[1] CRC[2]

        assert 0 <= bank <= 6, "bank should be in range [0, 6]"

        preset_addr = getattr(self, f"PRESETS_{self.preset}")
        cmd = [0x49, 0, 0, 0x40, 0x02]
        cmd += preset_addr
        cmd += [0, 0, 0x10, 0, 0, 0, bank]

        preset_addr = [(preset_addr[1] << 7) + preset_addr[0] - 2]
        checksum = self._get_checksum(preset_addr + [bank])
        cmd += self._pack_bytes(checksum.to_bytes(1, "little"), 1)

        self._send_sysex(cmd)
        self.bank = bank

    def change_preset(self, preset: int):
        # Message format:
        # - DEVID[3] 49 00 00 00 02 07 00 00 00 10 00 00 00 PRESET[1] CRC[2]

        assert 0 <= preset <= 3, "presets page should be in range [0, 3]"

        cmd = [0x49, 0, 0, 0, 0x02, 0x07, 0, 0, 0, 0x10, 0, 0, 0, preset]
        checksum = self._get_checksum([4, preset])
        cmd += self._pack_bytes(checksum.to_bytes(1, "little"), 1)

        self._send_sysex(cmd)
        self.preset = preset

    def led_off(self, pad, bank=None, preset=None):
        self.set_rgb_led(pad, 0, 0, 0, bank, preset)

    def set_led(self, pad):
        self.set_rgb_led(pad, 20, 20, 20)

    def set_rgb_led(self, pad, r, g, b, bank=None, preset=None):
        # Message format:
        # - DEVID[3] 59 00 00 40 02 ADDR[2] 00 00 30 00 00 00 R[1] G[1] B+CRC[1] CRC[1]

        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        color = (r, g, b)
        pad, bank, preset = self._clean_fields(pad, bank, preset)
        led_addr = self._get_prop_addr(pad, bank, preset, self.PROP_LED_OFFSET)

        cmd = [0x59, 0, 0, 0x40, 0x02]
        cmd += list(self._pack_bytes(led_addr.to_bytes(2, "little")))[:2]
        cmd += [0, 0, 0x30, 0, 0, 0]
        cmd += self._pack_bytes(bytes(color))

        checksum = self._get_checksum([led_addr] + list(color))
        cs_bytes = self._pack_bytes(checksum.to_bytes(1, "little"), 3)
        cmd[-1] |= cs_bytes[0]
        cmd.append(cs_bytes[1])

        self._send_sysex(cmd)

    def set_pad_mode(self, pad, mode: str, bank=None, preset=None):
        modes = {"pad": 0, "control": 1}
        assert mode in modes, f"mode must be one of {list(modes.keys())}"
        self._set_property(pad, [modes.get(mode)], self.PROP_MODE_OFFSET, bank, preset)

    def set_pad_type(self, pad, type: str, bank=None, preset=None):
        types = {"note": 0, "cc-toggle": 1, "momentary": 2, "program": 3, "custom": 4}
        assert type in types, f"type must be one of {list(types.keys())}"
        self._set_property(pad, [types.get(type)], self.PROP_TYPE_OFFSET, bank, preset)

    def set_pad_note(self, pad, note, bank=None, preset=None):
        assert 0 <= note <= 0x7F, "note number should be in range [0, 127]"
        self._set_property(pad, [note], self.PROP_NOTE_OFFSET, bank, preset)

    def set_pad_channel(self, pad, channel, bank=None, preset=None):
        assert 0 <= channel <= 15, "channel should be in range [0, 15]"
        self._set_property(pad, [channel], self.PROP_CHANNEL_OFFSET, bank, preset)

    def _set_property(self, pad, value: list, offset, bank=None, preset=None):
        # Message format:
        # - DEVID[3] 49 00 00 40 02 ADDR[2] 00 00 10 00 00 00 VALUE[1] CRC[2]

        pad, bank, preset = self._clean_fields(pad, bank, preset)
        prop_addr = self._get_prop_addr(pad, bank, preset, offset)

        cmd = [0x49, 0, 0, 0x40, 0x02]
        cmd += list(self._pack_bytes(prop_addr.to_bytes(2, "little")))[:2]
        cmd += [0, 0, 0x10, 0, 0, 0] + value

        checksum = self._get_checksum([0xFE, prop_addr] + value)
        cmd += self._pack_bytes(checksum.to_bytes(1, "little"), 1)

        self._send_sysex(cmd)

    def sync(self):
        # Message format:
        # - DEVID[3] 41 00 00 00 02 00 00 00 00 00 01 00 00 73 01

        self._synced.clear()
        self._send_sysex("41 00 00 00 02 00 00 00 00 00 01 00 00 73 01", self.DEVID_STAT)
        if not self._synced.wait(timeout=5):
            print("WARNING: could not sync, status not received (timeout)")

    def _send_sysex(self, cmd, devid=DEVID_CTRL, debug=False):
        if isinstance(cmd, str):
            cmd = bytes.fromhex(cmd)
        elif isinstance(cmd, (list, tuple)):
            cmd = bytes(cmd)
        data = bytes(devid) + cmd
        if debug or self._debug:
            print(f"SysEx out:")
            hexdump(data)
        msg = mido.Message(type="sysex", data=data)
        self._port.send(msg)

        # NOTE: I see a problem when sending two messages too quickly, neither of them
        # arrived. Adding a little wait here appears to fix it.
        if self._wait_on_send:
            time.sleep(0.001)

    def _recv_sysex(self, data):
        # Message format:
        # - DEVID[3] 01 01 00 00 02 00 00 00 00 00 01 00 00 20 01 58 11 00 00 00 00
        # - PRESET[1] CRC[2]

        if self._debug:
            print(f"SysEx in:")
            hexdump(bytes(data))

        if data[3:8] == (1, 1, 0, 0, 2):
            self.preset = data[-3]
            self._synced.set()

    def _clean_fields(self, pad, bank, preset):
        bank = bank if bank is not None else self.bank
        preset = preset if preset is not None else self.preset

        assert 0 <= preset <= 3, f"preset ({preset}) should be in range [0, 3]"
        assert 0 <= bank <= 6, f"bank ({bank}) should be in range [0, 6]"
        assert 0 <= pad <= 15, f"pad ({pad}) should be in range [0, 15]"

        return pad, bank, preset

    def _get_prop_addr(self, pad, bank, preset, offset):
        # 19: distance between presets
        # 26: distance between pads
        # 16: number of pads
        # 7: number of banks
        # 2916: distance between presets for PAD mode addressing

        # print(f"PAD: {preset}.{bank}.{pad}, offset: {offset}")
        if offset == self.PROP_MODE_OFFSET:
            return offset + (2916 + 15) * preset + pad
        return offset + 19 * preset + (preset * 7 * 16 + bank * 16 + pad) * 26

    def _get_checksum(self, data: list):
        magic = 0xF7
        ds = 0
        for x in data:
            y = x
            while y > 0:
                ds += (y & 0xFF)
                y >>= 8
        return (magic - (ds & 0xFF)) & 0xFF

    def _pack_bytes(self, data: bytes, bit_offset: int = 0):
        retval = [0]
        for b in data:
            retval[-1] |= (b << bit_offset) & 0x7F
            retval.append(b >> (7 - bit_offset))
            bit_offset += 1
            if bit_offset > 6:
                bit_offset = 0

        return bytes(retval)
