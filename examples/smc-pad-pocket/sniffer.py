#!/usr/bin/env python3

import mido

# List available input ports
input_ports = mido.get_input_names()
if not input_ports:
    print("No MIDI input ports found.")
    exit()

print("Available MIDI input ports:")
for i, name in enumerate(input_ports):
    print(f"{i + 1}: {name}")

# Ask the user to choose a port
while True:
    try:
        choice = int(input("\nSelect the number of the port to use: ")) - 1
        if 0 <= choice < len(input_ports):
            MIDI_IN_PORT = input_ports[choice]
            break
        else:
            print("Invalid number, please try again.")
    except ValueError:
        print("Please enter a valid number.")

print(f"\nListening for messages on {MIDI_IN_PORT}... (Ctrl+C to exit)\n")

# Manufacturer ID to filter
TARGET_MANUFACTURER = [0x00, 0x32, 0x09]

# Open the port and listen for messages
with mido.open_input(MIDI_IN_PORT) as inport:
    try:
        for msg in inport:
            if msg.type == 'sysex':
                data = list(msg.data)
                if data[:3] == TARGET_MANUFACTURER:
                    sysex_bytes = [0xF0] + data + [0xF7]
                    print(' '.join(f'{b:02X}' for b in sysex_bytes))
    except KeyboardInterrupt:
        print("\nStopped by user")
