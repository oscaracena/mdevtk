# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2025, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from threading import Event

import mido

from ..controller import DeviceController
try:
    from hexdump import hexdump
except ImportError:
    hexdump = print


class SMCPadPocket(DeviceController):
    DEVID_CTRL      = [0x00, 0x32, 0x09]
    DEVID_STAT      = [0x00, 0x32, 0x0D]

    PRESETS_0       = [0x70, 0x16]
    PRESETS_1       = [0x63, 0x2D]
    PRESETS_2       = [0x56, 0x44]
    PRESETS_3       = [0x49, 0x5B]

    def __init__(self, note_start=36, channel=9):
        super().__init__("SMC-PAD Pocket-Private")
        self._synced = Event()

        # public properties
        self.preset = 0
        self.bank = 0

        self.on_sysex(self.DEVID_STAT, self._recv_sysex)
        for col in range(4):
            for row in range(4):
                pad = row * 4 + col
                note = note_start + pad
                self.on_note(
                    channel=channel, note=note, cb="on_pad",
                    pad=pad, row=row, col=col)

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

    def set_rgb_led(self, pad, r, g, b, bank=0):
        # Message format:
        # - DEVID[3] 59 00 00 40 02 ADDR[2] 00 00 30 00 00 00 R[1] G[1] B+CRC[1] CRC[1]

        assert 0 <= bank <= 6, "bank should be in range [0, 6]"
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        color = (r, g, b)
        cmd = [0x59, 0, 0, 0x40, 0x02]
        cmd += self._get_pad_addr(bank, pad)
        cmd += [0, 0, 0x30, 0, 0, 0]
        cmd += self._pack_bytes(bytes(color))

        pad_no = 5 + (bank * 16 + pad) * 26
        checksum = self._get_checksum([pad_no] + list(color))
        cs_bytes = self._pack_bytes(checksum.to_bytes(1, "little"), 3)
        cmd[-1] |= cs_bytes[0]
        cmd.append(cs_bytes[1])

        self._send_sysex(cmd)

    def sync(self):
        # Message format:
        # - DEVID[3] 41 00 00 00 02 00 00 00 00 00 01 00 00 73 01

        self._synced.clear()
        self._send_sysex("41 00 00 00 02 00 00 00 00 00 01 00 00 73 01", self.DEVID_STAT)
        self._synced.wait()

    def _send_sysex(self, cmd, devid=DEVID_CTRL, debug=False):
        if isinstance(cmd, str):
            cmd = bytes.fromhex(cmd)
        elif isinstance(cmd, (list, tuple)):
            cmd = bytes(cmd)
        data = bytes(devid) + cmd
        if debug:
            print(f"SysEx:")
            hexdump(data)
        msg = mido.Message(type="sysex", data=data)
        self._port.send(msg)

    def _recv_sysex(self, data):
        # Message format:
        # - DEVID[3] 01 01 00 00 02 00 00 00 00 00 01 00 00 20 01 58 11 00 00 00 00
        # - PRESET[1] CRC[2]

        if data[3:8] == (1, 1, 0, 0, 2):
            self.preset = data[-3]
            self._synced.set()

    def _get_pad_addr(self, bank: int, pad: int, offset: int = 5):
        n_pad = bank * 16 + pad
        b1 = offset + (n_pad * 26) % 0x80
        b2 = n_pad // 5
        return [b1, b2]

    def _get_checksum(self, data: bytes):
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
