#!/usr/bin/env python3

import mido
from pathlib import Path
from argparse import ArgumentParser

from mdevtk.controller import DeviceController


class Mapper:
    def __init__(self, args):
        self._dev_id = args.device_name
        self._class_name = args.class_name
        self._note_map = {}
        self._cc_map = {}

    def on_note(self, msg, name, send_value):
        self._note_map[(msg.channel, msg.note)] = (name, send_value)

    def on_cc(self, msg, name):
        self._cc_map[(msg.channel, msg.control)] = name

    def build(self):
        if not self._class_name:
            self._class_name = input("Class name? ") or "ClassName"

        retval = self._strip_pad("""\
        # -*- mode: python; coding: utf-8 -*-\n
        from ..controller import DeviceController\n\n
        class {class_name}(DeviceController):
            def __init__(self):
                super().__init__("{dev_id}")\n
        """.format(class_name=self._class_name, dev_id=self._dev_id), 8)

        for n, i in self._note_map.items():
            send_value = ", send_value=True" if i[1] else ""
            cmd = f'self.on_note(channel={n[0]}, note={n[1]}, cb="on_{i[0]}"{send_value})\n'
            retval += self._add_pad(cmd, 8)

        retval += "\n"
        for n, i in self._cc_map.items():
            cmd = f'self.on_cc(channel={n[0]}, controls={(n[1],)}, cb="on_{i[0]}")\n'
            retval += self._add_pad(cmd, 8)

        return retval

    def _strip_pad(self, s, pad):
        return "\n".join(l[pad:] for l in s.split("\n"))

    def _add_pad(self, s, pad):
        return " " * pad + s


class CaptureController(DeviceController):
    def __init__(self, args):
        super().__init__(args.device_name)
        self._args = args
        self._mapper = Mapper(args)
        print(f"Using device name:\n - {self._port.name}")
        print("Start pressing keys on your MIDI controller, and give them a name")
        print("Press Ctrl+C when finished.\n---")

    def _on_message(self, msg):
        if msg.type == "note_on":
            pr = f"on note, C:{msg.channel}, N:{msg.note}, [NAME, send_value?]: "
            fields = input(pr).split()
            if not fields:
                return
            name = fields[0]
            send_value = len(fields) > 1 and fields[1] == "1"
            self._mapper.on_note(msg, name, send_value)

        elif msg.type == "control_change":
            pr = f"on control, C:{msg.channel}, CTR:{msg.control}, NAME: "
            fields = input(pr).split()
            if not fields:
                return
            name = fields[0]
            self._mapper.on_cc(msg, name)

    def write(self):
        outfile = Path(self._args.output_filename)
        if outfile.exists() and not self._args.force_overwrite:
            overwrite = input(f"File {outfile.as_posix()} exists, overwrite it? (y/N) ")
            if overwrite.lower() != "s":
                print("NOT overwrite, nothing done.")
                return

        content = self._mapper.build()
        with outfile.open("w") as dst:
            dst.write(content)

        print(f"\nFile {outfile.as_posix()} writen!")
        print("Remember that this file should be inside 'devices' folder of mdevtk.")


class MonitorController(DeviceController):
    def __init__(self, args):
        super().__init__(args.device_name)
        self._args = args
        print(f"Using device name:\n - {self._port.name}")
        print("Start pressing keys on your MIDI controller.")
        print("Press Ctrl+C when finished...")

    def _on_message(self, msg):
        print(msg)


class DevCapturer:
    def __init__(self, args):
        self._args = args

    def run(self):
        if args.list_devices:
            self._cmd_list_devices()
        elif args.monitor:
            self._cmd_monitor_mode()
        elif args.generate:
            self._cmd_generate()
        else:
            print("No action given. Add -h for a list of available options.")

    def _cmd_generate(self):
        if not self._args.device_name:
            print("ERROR, you must provide the device name")
            return

        self._dev = CaptureController(self._args)
        try:
            self._dev.loop()
        except KeyboardInterrupt:
            print("\r---")
            self._dev.write()

    def _cmd_monitor_mode(self):
        if self._args.device_name is None:
            parser.error("monitor mode requires --device-name")

        self._dev = MonitorController(self._args)
        try:
            self._dev.loop()
        except KeyboardInterrupt:
            print("\rBye!")

    def _cmd_list_devices(self):
        devs = mido.get_output_names()
        if not devs:
            print("No devices detected!")
            return

        print("Devices detected:")
        for name in devs:
            print(f"- {name}")


if __name__ == "__main__":
    parser = ArgumentParser()
    actions = parser.add_argument_group(title="actions")

    # actions
    actions.add_argument("-l", "--list-devices", action="store_true",
        help="list current connected devices")
    actions.add_argument("-g", "--generate", action="store_true",
        help="start the generation of device driver")
    actions.add_argument("-m", "--monitor", action="store_true",
        help="start in monitor mode, it just listen for events")

    # options
    parser.add_argument("-d", "--device-name",
        help="name of device to connect to")
    parser.add_argument("-o", "--output-filename", default="gen-device.py",
        help="path to output filename")
    parser.add_argument("-f", "--force-overwrite", action="store_true",
        help="do not ask if output filename exists, overwrite it")
    parser.add_argument("-c", "--class-name",
        help="name of generated class")

    args = parser.parse_args()
    dc = DevCapturer(args)
    dc.run()
