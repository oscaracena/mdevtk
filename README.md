# Intro

This is MIDI Device ToolKit (mdevtk). The aim of this Python library is to handle MIDI events from a controller (and let the user choose what to do), and send back MIDI events to control it back (for instance, the LED lights of a DJControl Starlight).

Just that.


# Installing requirements

As always with Python, install them using pip, or using your system's package manager. Using pip is easy:

    pip install -r requirements.txt


# Usage

This library is object oriented. Thus, in order to manage a specific device, you need to create an instance of the corresponding class. Moreover, the controller sends its events through method callbacks, so in order to receive them, you need to subclass it. It's easier than it sounds, I promise.

Let's see an example. I have a Hercules DJControl Starlight, so the class that I will import is called `DJControlStarlight`. I want to detect when the button `PLAY` of the left deck (also called Deck A or 1) is pressed, so I will implement the method `on_left_play`. Something like this:

```python
from mdevtk import DJControlStarlight

class MyDJControl(DJControlStarlight):
    def on_left_play(self):
        print("PLAY of deck A pressed!")
```

Now, what remains is just to create an instance of that class, and wait. This last bit (the *waiting*) could be done in many ways. For instance, your application may be busy doing other things. Or you have an event loop that needs to be run. Or you may sleep using `time.sleep()`... If you don't have any other thing to do, just use the `loop()` method of the class (which is a *sleep* inside a *while True*):

```python
device = MyDJControl()
device.loop()
```

And that's it! Put that code in a file (I called it `play-test.py`), run it and see what happens when you press the PLAY in the controller:

```shell
> python3 play-test.py
PLAY of deck A pressed!
PLAY of deck A pressed!
PLAY of deck A pressed!
```

It's easy, isn't it? Now, the collection of methods that you can implement to receive events depends on the device created. You can see the code.

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
