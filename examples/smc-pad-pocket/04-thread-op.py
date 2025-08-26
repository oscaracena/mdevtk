#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2025, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import sys
import time
from threading import Event
from queue import Queue
from mdevtk import SMCPadPocket


# Set WAIT_ACK to False, in order to use the internal sleep when sending
# Set WAIT_ACK to True, to wait for an ACK before sending next message
WAIT_ACK = True
if len(sys.argv) > 1:
    WAIT_ACK = sys.argv[1] == "1"


class MySMCPadPocket(SMCPadPocket):
    NOTE_START = 0
    CHANNEL    = 0
    X          = 127
    COLORS     = [
        (X, X, X), (X, X, 0), (X, 0, X), (X, 0, 0),
        (0, X, X), (0, X, 0), (0, 0, X), (0, 0, 0),
    ]

    def __init__(self):
        super().__init__(self.NOTE_START, self.CHANNEL)
        self.sync()
        self._setup_ctrl()
        if not WAIT_ACK:
            self._wait_on_send = True

        self._idx = 0
        self._acked = Event()
        self._messages = Queue()
        self._start_ts = None

        self.on_sysex(self.DEVID_ACK, self._recv_ack)

    # NOTE: we use the main thread to send messages, and the MIDI thread to
    # receive them
    def loop(self):
        counter = 0
        while True:
            pad, color = self._messages.get()
            self._acked.clear()
            self.set_rgb_led(pad, *color)
            self._acked.wait()

            counter += 1
            if counter >= 16:
                elapsed = (time.monotonic() - self._start_ts) * 1000
                print(f"done! [{elapsed:.3f} ms]")
                counter = 0

    def _setup_ctrl(self):
        self.change_preset(0)
        self.change_bank(0)

        for pad in range(16):
            self.set_pad_mode(pad, "pad")
            self.set_pad_type(pad, "note")
            self.set_pad_note(pad, self.NOTE_START + pad)
            self.set_pad_channel(pad, self.CHANNEL)
            self.led_off(pad)

    def _recv_ack(self, data):
        ack = "00 32 01 08 00 00 00 00 7F 01"
        if bytes(data) == bytes.fromhex(ack):
            self._acked.set()

    def fill(self, color):
        for pad in range(16):
            if WAIT_ACK:
                self._messages.put_nowait((pad, color))
            else:
                self.set_rgb_led(pad, *color)

    # NOTE: this method occupies the MIDI thread, so any ACK will be received
    # after this
    def on_pad(self, pad, row, col):
        if not self._synced.is_set():
            return

        self._start_ts = time.monotonic()
        color = self.COLORS[self._idx]
        self._idx = (self._idx + 1) % len(self.COLORS)
        print(f"> Filling with color {[f'{c:03}' for c in color]}...", end="", flush=True)
        self.fill(color)

        if not WAIT_ACK:
            elapsed = (time.monotonic() - self._start_ts) * 1000
            print(f"done! [{elapsed:.3f} ms]")


try:
    device = MySMCPadPocket()
    print(f"> WAIT ACK: {WAIT_ACK}")
    print("Ready! Press any PAD on your controller...")
    device.loop()
except KeyboardInterrupt:
    print("\rBye!")
