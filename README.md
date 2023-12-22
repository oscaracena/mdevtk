# Intro

This is MIDI Device ToolKit (mdevtk). The aim of this Python library is to handle MIDI events from a controller (and let the user choose what to do), and send back MIDI events to control it back (for instance, the LED lights of a DJControl Starlight).

Just that.


# Installing requirements

As always with Python, install them using pip, or using your system's package manager. Using pip is easy:

    pip install -r requirements.txt


# Usage


# Running examples

First, source the file `set-env.sh` to update the `PYTHONPATH` variable. Then, just run the selected example from the root folder. Like this:

    source set-env.sh
    python3 examples/djcontrol-starlight/01-on-shift-press.py


# References & other info

## MIDI

* https://www.songstuff.com/recording/article/midi_message_format/

## Hercules DJControl Starlight

* https://www.hercules.com/es/product/djcontrol-starlight/
* https://github.com/mixxxdj/mixxx/blob/main/res/controllers/Hercules%20DJControl%20Starlight.midi.xml
