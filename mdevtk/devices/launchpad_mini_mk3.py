# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2024, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import mido

from ..controller import DeviceController
try:
    from hexdump import hexdump
except ImportError:
    hexdump = print


class LaunchpadMiniMK3(DeviceController):

    SYSEX_HEADER      = bytes.fromhex("00 20 29 02 0D")

    LAYOUT_SESSION    = 0x00
    LAYOUT_DRUMS      = 0x04
    LAYOUT_KEYS       = 0x05
    LAYOUT_USER       = 0x06

    LED_STOP          = 19
    LED_SESSION_START = 19
    LED_SESSION_END   = 89
    LED_UP            = 91
    LED_DOWN          = 92
    LED_LEFT          = 93
    LED_RIGHT         = 94
    LED_LOGO          = 99

    LIGHT_STATIC      = 0
    LIGHT_FLASHING    = 1
    LIGHT_PULSING     = 2
    LIGHT_RGB         = 3

    def __init__(self):
        super().__init__("LPMiniMK3 DA")
        self._enable_daw_mode(True)
        self.select_layout(self.LAYOUT_SESSION)

        for col in range(8):
            for row in range(8):
                pad = row * 8 + col
                note = 10 * (row + 1) + col + 1
                self.on_note(channel=0, note=note, cb="on_pad", pad=pad, row=row, col=col)

        self.on_cc(channel=0, controls=91, cb="on_up", send_value=False, note_off=False)
        self.on_cc(channel=0, controls=92, cb="on_down", send_value=False, note_off=False)
        self.on_cc(channel=0, controls=93, cb="on_left", send_value=False, note_off=False)
        self.on_cc(channel=0, controls=94, cb="on_right", send_value=False, note_off=False)
        self.on_cc(channel=0, controls=95, cb="on_session_mode", send_value=False, note_off=False)
        self.on_cc(channel=0, controls=96, cb="on_drums_mode", send_value=False, note_off=False)
        self.on_cc(channel=0, controls=97, cb="on_keys_mode", send_value=False, note_off=False)
        self.on_cc(channel=0, controls=98, cb="on_user_mode", send_value=False, note_off=False)

        for idx, cc in enumerate(range(19, 90, 10)):
            self.on_cc(channel=0, controls=cc, cb="on_session",
                       send_value=False, note_off=False, num=idx)

    def close(self):
        self._enable_daw_mode(False)

    def select_layout(self, layout):
        self._send_sysex(f"00 {layout:02X}")

    def led_on(self, led_id, color=41):
        self.set_led(led_id, color)

    def led_off(self, led_id):
        self.set_led(led_id, 0)

    def set_led(self, led_id, color=0):
        if led_id > 88 or str(led_id)[1:] == "9":
            msg = mido.Message(type="control_change", channel=0, control=led_id, value=color)
        else:
            msg = mido.Message(type="note_on", channel=0, note=led_id, velocity=color)
        # print(msg)
        self._port.send(msg)

    def print(self, text, loop=False, speed=3, color=41):
        cmd = [7, int(loop), speed, 0, color] + list(map(ord, text))
        self._send_sysex(" ".join(f"{b:02X}" for b in cmd))

    def print_clear(self):
        self._send_sysex("07")

    def setup_faders(self, faders, vertical=True):
        assert len(faders) <= 8, "There could only be 8 faders!"
        msg = f"01 00 0{'0' if vertical else '1'}"
        for index, f in enumerate(faders):
            msg += f"{index:02X}"
            if f is None:
                msg += f"00 {index:02X} 00"
                continue
            msg += '01' if f.get("bipolar", False) else '00'
            cc = int(f.get("cc", index))
            msg += f"{cc:02X}"
            msg += f'{min(127, max(0, int(f.get("color", 37)))):02X}'

            name = f.get("name", f"fader_{index}")
            self.on_cc(channel=4, controls=cc, cb=f"on_{name}_change")

        self._send_sysex(msg)

    def show_faders(self):
        self._send_sysex("00 0D")

    def hide_faders(self):
        self._send_sysex("00 00")

    def _enable_daw_mode(self, enabled=True):
        self._send_sysex(f"10 0{1 if enabled else 0}")

    def _send_sysex(self, cmd, debug=False):
        cmd = bytes.fromhex(cmd)
        if debug:
            print(f"SysEx:")
            hexdump(self.SYSEX_HEADER + cmd)
        msg = mido.Message(type="sysex", data=self.SYSEX_HEADER + cmd)
        self._port.send(msg)
