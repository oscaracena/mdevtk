# Intro

This is MIDI Device ToolKit (mdevtk). The aim of this Python library is to handle MIDI events from a controller (let the user choose what to do), and send back MIDI events to control it (for instance, the LED lights of a DJControl Starlight).

Just that.


# Installing requirements

As always with Python, install them using pip, or using your system's package manager. With pip is easy:

    pip install -r requirements.txt


# Usage

## Receiving events

This library is object oriented. Thus, in order to manage a specific device, you need to create an instance of the corresponding class. Moreover, the controller sends its events through method callbacks, so in order to receive them, you need to subclass it. It's easier than it sounds, I promise.

Let's see an example. I have a Hercules DJControl Starlight, so the class that I will import is called `DJControlStarlight`. I want to detect when the button `PLAY` of the left deck (also called Deck A or 1) is pressed, so I will implement the method `on_left_play`. Something like this:

```python
from mdevtk import DJControlStarlight

class MyDJControl(DJControlStarlight):
    def on_left_play(self):
        print("PLAY of deck A pressed!")
```

Now, what remains is just to create an instance of that class, and wait. This last bit (the *waiting*) could be done in many ways. For instance, your application may be busy doing other things. Or you have an event loop that needs to be run. Or you may sleep using `time.sleep()`... If you don't have any other thing to do, just use the helper method `loop()` (which is a *sleep* inside a *while True*):

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

It's easy, isn't it? Now, the collection of methods that you can implement to receive events depends on the device created. You can see the list of [methods for the DJControl Starlight](docs/djcontrol-starlight.md).


## Controling LEDs

If your hardware has LEDs on it (and support for controlling them), you can lit them on! Use the device functions `led_on()` and `led_off()`. Or, if you prefer, call `set_led()` giving the desired state (ON=`True`, OFF=`False`). Let's see an example of use (again, with the DJControl Starlight):

```python
from mdevtk import DJControlStarlight

device = DJControlStarlight()
device.led_on(device.LEFT_SYNC)
```

With that 3 lines of code, you will switch on the Bank A SYNC button. Amazing! :) You can switch them on, off... or even blink them, using the method `led_blink()`. It will return an object to control the linking status: you can `pause()`, `play()`, `stop()` and `set_speed()` on that object. For example:

```python
import time
from mdevtk import DJControlStarlight

device = DJControlStarlight()

blinker = device.led_blink(device.LEFT_PLAY, speed=3)
time.sleep(5)
blinker.set_speed(9)
time.sleep(5)
blinker.stop()
```

## Switching between banks (from software)

Again, if your hardware supports it, you can change the selected bank. The DJControl, for instance, has 4 banks on each deck. And each bank has 4 pads, whith independient LED controls and events. Switch between them using the method `change_bank()`. For example:

```python
from mdevtk import DJControlStarlight

device = DJControlStarlight()
device.change_bank(device.LEFT_MODE_SAMPLER)
device.led_on(device.LEFT_SAMPLER_1)
```

# Running the examples

First, source the file `set-env.sh` to update the `PYTHONPATH` variable. Then, just run the selected example from the root folder. Like this:

    source set-env.sh
    python3 examples/djcontrol-starlight/01-on-shift-press.py


# References & other info

## MIDI

* https://www.songstuff.com/recording/article/midi_message_format/

## Hercules DJControl Starlight

* https://www.hercules.com/es/product/djcontrol-starlight/
* https://github.com/mixxxdj/mixxx/blob/main/res/controllers/Hercules%20DJControl%20Starlight.midi.xml
