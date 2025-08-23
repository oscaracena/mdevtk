#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2025, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import readline
from mdevtk import SMCPadPocket


device = SMCPadPocket()
device.sync()

print("Enter 'B<n>' to change bank (1-7) or 'P<n>' to change preset (1-4).")
while True:
    try:
        cmd = input(f"P:{device.preset + 1}, B:{device.bank + 1}> ")
        cmd = cmd.strip().upper()

        if cmd.startswith('B'):
            device.change_bank(int(cmd[1:]) - 1)
        elif cmd.startswith('P'):
            device.change_preset(int(cmd[1:]) - 1)
        else:
            print("Invalid command.")
    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nBye!")
        break
