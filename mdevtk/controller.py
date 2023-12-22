# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import time
import mido

from .exceptions import NoDeviceFound
from .utils import log


class NoteCallback:
    def __init__(self, controller, cb_name):
        self._handler = getattr(controller, cb_name, None)

    def __call__(self, *args, **kwargs):
        if self._handler is None:
            return
        try:
            self._handler(*args, **kwargs)
        except Exception as err:
            log.error(f" invalid callback: {err}")


class CCCallback:
    def __init__(self, controller, cb_name, controls):
        self._handler = getattr(controller, cb_name, None)
        self._controls = controls  # MSB, LSB
        self._bytes = {}

    def __call__(self, msg, *args, **kwargs):
        if self._handler is None:
            return

        # if byte is not LSB, just store it
        byte_idx = self._controls.index(msg.control)
        self._bytes[byte_idx] = msg.value
        if byte_idx != 0:
            return

        # on LSB, then call handler and restart
        value = 0
        for k, v in self._bytes.items():
            value += v * (127 ** k)
        self._bytes = {}

        try:
            self._handler(value, *args, **kwargs)
        except Exception as err:
            log.error(f" invalid callback: {err}")


class DeviceController:
    # LED commands, overwrite in derived controller if different
    CMD_LED_ON  = 0x01
    CMD_LED_OFF = 0x00

    def __init__(self, dev_id):
        self._mapping = {}

        name = self._find_device(dev_id)
        if name is None:
            raise NoDeviceFound(dev_id)

        self._port = mido.open_ioport(name, callback=self._on_message)

    def __del__(self):
        self._port.close()

    def loop(self):
        while True:
            time.sleep(0.1)

    def led_on(self, led_id):
        self.set_led(led_id, True)

    def led_off(self, led_id):
        self.set_led(led_id, False)

    def set_led(self, led_id, status):
        channel, note = led_id
        cmd = self.CMD_LED_ON if status else self.CMD_LED_OFF
        msg = mido.Message(type="note_on", channel=channel, note=note, velocity=cmd)
        self._port.send(msg)

    def on_note(self, channel, note, cb):
        cb = NoteCallback(self, cb)
        msg = mido.Message(type="note_on", channel=channel, note=note)
        self._mapping[self._msg_id(msg)] = cb

    def on_cc(self, channel, controls, cb):
        cb = CCCallback(self, cb, controls)
        for ctrl in controls:
            msg = mido.Message(type="control_change", channel=channel, control=ctrl)
            self._mapping[self._msg_id(msg)] = cb

    def _on_message(self, msg):
        args = []
        if msg.type == "note_on":
            if msg.velocity == 0:
                return
        elif msg.type == "control_change":
            args.append(msg)
        else:
            return

        callback = self._mapping.get(self._msg_id(msg))
        if callback is None:
            return

        callback(*args)

    def _find_device(self, id):
        devices = mido.get_output_names()
        for name in devices:
            if id in name:
                return name

    def _msg_id(self, msg):
        return bytes(msg.bytes()[:2])
