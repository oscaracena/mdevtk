# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from threading import Thread
import time
import mido

from .exceptions import NoDeviceFound
from .utils import log


# FIXME: Refactor & DRY these Callbacks!

class NoteCallback:
    def __init__(self, controller, callback, send_value=False, kwargs={}):
        if not callable(callback):
            callback = getattr(controller, callback, None)
        self._handler = callback
        self._send_value = send_value
        self._kwargs = kwargs

    def __call__(self, msg):
        if self._handler is None:
            return

        try:
            args = [msg] if self._send_value else []
            self._handler(*args, **self._kwargs)
        except Exception as err:
            log.error(f" invalid callback: {err}")


class AfterTouchCallback:
    def __init__(self, controller, callback, kwargs={}):
        if not callable(callback):
            callback = getattr(controller, callback, None)
        self._handler = callback
        self._kwargs = kwargs

    def __call__(self, msg):
        if self._handler is None:
            return

        try:
            self._handler(msg.value, **self._kwargs)
        except Exception as err:
            log.error(f" invalid callback: {err}")


class PitchWheelCallback:
    def __init__(self, controller, callback, kwargs={}):
        if not callable(callback):
            callback = getattr(controller, callback, None)
        self._handler = callback
        self._kwargs = kwargs

    def __call__(self, msg):
        if self._handler is None:
            return

        try:
            self._handler(msg.pitch, **self._kwargs)
        except Exception as err:
            log.error(f" invalid callback: {err}")


class PCCallback:
    def __init__(self, controller, callback, kwargs={}):
        if not callable(callback):
            callback = getattr(controller, callback, None)
        self._handler = callback
        self._kwargs = kwargs

    def __call__(self, msg):
        if self._handler is None:
            return

        try:
            self._handler(msg.program, **self._kwargs)
        except Exception as err:
            log.error(f" invalid callback: {err}")


class CCCallback:
    def __init__(self, controller, cb_name, controls, kwargs):
        self._handler = getattr(controller, cb_name, None)
        self._controls = controls  # MSB, LSB
        self._bytes = {}
        self._kwargs = kwargs

    def __call__(self, msg):
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
            self._handler(value, **self._kwargs)
        except Exception as err:
            log.error(f" invalid callback: {err}")


class LedBlinker(Thread):
    # NOTE: Multiple threads can safely send and receive notes on the same port.

    def __init__(self, ctrl, led_id, speed):
        super().__init__()
        self.daemon = True

        self._should_stop = False
        self._is_paused = False
        self._ctrl = ctrl
        self._led_id = led_id
        self._led_is_on = False
        self.set_speed(speed)
        self.start()

    def run(self):
        while not self._should_stop:
            if not self._is_paused:
                self._led_is_on = not self._led_is_on
                self._ctrl.set_led(self._led_id, self._led_is_on)
            q = 1 / self.speed
            time.sleep(q)

    def stop(self):
        self.pause()
        self._should_stop = True

    def pause(self):
        self._ctrl.set_led(self._led_id, False)
        self._is_paused = True

    def play(self):
        self._is_paused = False

    def set_speed(self, speed):
        self.speed = max(0, speed)


class DeviceController:
    # Control commands, overwrite in derived controller if different
    CMD_LED_ON   = 0x01
    CMD_LED_OFF  = 0x00
    CMD_CHANGE_BANK = 0x01

    def __init__(self, dev_id):
        self._mapping = {}

        name = self._find_device(dev_id)
        if name is None:
            raise NoDeviceFound(dev_id)

        self._port = mido.open_ioport(name, callback=self._on_message)

    def __del__(self):
        if hasattr(self, "_port"):
            self._port.close()

    def loop(self):
        while True:
            time.sleep(0.1)

    def led_on(self, led_id):
        self.set_led(led_id, True)

    def led_off(self, led_id):
        self.set_led(led_id, False)

    def led_blink(self, led_id, speed=3):
        return LedBlinker(self, led_id, speed)

    def set_led(self, led_id, status):
        if not isinstance(led_id, (tuple, list)):
            led_id = (0, led_id)

        channel, note = led_id
        cmd = self.CMD_LED_ON if status else self.CMD_LED_OFF
        msg = mido.Message(type="note_on", channel=channel, note=note,
            velocity=cmd)
        self._port.send(msg)

    def set_rgb_led(self, led_id, r, g, b):
        channel, note = led_id
        msg = mido.Message(type="note_on", channel=channel, note=note,
            velocity=self._rgb_to_value(r, g, b))
        self._port.send(msg)

    def change_bank(self, msg):
        channel, note = msg
        msg = mido.Message(type="note_on", channel=channel, note=note,
            velocity=self.CMD_CHANGE_BANK)
        self._port.send(msg)

    def on_note(self, channel, note, cb, send_value=False, **kwargs):
        cb = NoteCallback(self, cb, send_value, kwargs)
        msg = mido.Message(type="note_on", channel=channel, note=note)
        self._mapping[self._msg_id(msg)] = cb

    def on_pc(self, channel, program, cb, **kwargs):
        cb = PCCallback(self, cb, kwargs)
        msg = mido.Message(type="program_change", channel=channel, program=program)
        self._mapping[self._msg_id(msg)] = cb

    def on_cc(self, channel, controls, cb, **kwargs):
        cb = CCCallback(self, cb, controls, kwargs)
        for ctrl in controls:
            msg = mido.Message(type="control_change", channel=channel, control=ctrl)
            self._mapping[self._msg_id(msg)] = cb

    def on_aftertouch(self, channel, cb, **kwargs):
        cb = AfterTouchCallback(self, cb, kwargs)
        msg = mido.Message(type="aftertouch", channel=channel)
        self._mapping[self._msg_id(msg, 1)] = cb

    def on_pitchwheel(self, channel, cb, **kwargs):
        cb = PitchWheelCallback(self, cb, kwargs)
        msg = mido.Message(type="pitchwheel", channel=channel)
        self._mapping[self._msg_id(msg, 1)] = cb

    def _on_message(self, msg):
        sig_bytes = 2
        if msg.type == "note_on":
            if msg.velocity == 0:
                return
        elif msg.type in ("aftertouch", "pitchwheel"):
            sig_bytes = 1
        elif msg.type not in ("program_change", "control_change"):
            return

        callback = self._mapping.get(self._msg_id(msg, sig_bytes))
        if callback is not None:
            callback(msg)

    def _rgb_to_value(self, r, g, b):
        # NOTE: overwrite this method to implement a suitable conversion.
        return r + g + b

    def _find_device(self, id):
        devices = mido.get_output_names()
        for name in devices:
            if id in name:
                return name

    def _msg_id(self, msg, num_bytes=2):
        return bytes(msg.bytes()[:num_bytes])
