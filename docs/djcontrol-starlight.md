# Hercules DJControl Starlight

> Class name: `DJControlStarlight`

Buttons, sliders, pots, jog wheels and LEDs are supported.


## Event methods

### `note-on` events

Sent on button press. Methods without arguments.

| Method name            | Control element                                    |
|------------------------|----------------------------------------------------|
|`on_bass_filter_toggle` | Toggle between filter & bass for channel 1/2       |
|`on_shift`              | Shift button to select alternate button functions  |
|`on_left_sync`          | Deck A SYNC button                                 |
|`on_left_cue`           | Deck A CUE button                                  |
|`on_left_play`          | Deck A PLAY button                                 |
|`on_left_wheel_touch`   | Deck A jog wheel surface touch                     |
|`on_left_headphones`    | Deck A headphones button                           |
|`on_left_hot_cue`       | Deck A HOT CUE bank selected                       |
|`on_left_loop`          | Deck A LOOP bank selected                          |
|`on_left_fx`            | Deck A FX bank selected                            |
|`on_left_sampler`       | Deck A SAMPLER bank selected                       |
|`on_vinyl`              | Vinyl button                                       |
|`on_right_sync`         | Deck B SYNC button                                 |
|`on_right_cue`          | Deck B CUE button                                  |
|`on_right_play`         | Deck B PLAY button                                 |
|`on_right_wheel_touch`  | Deck B jog wheel surface touch                     |
|`on_right_headphones`   | Deck B headphones button                           |
|`on_right_hot_cue`      | Deck B HOT CUE bank selected                       |
|`on_right_loop`         | Deck B LOOP bank selected                          |
|`on_right_fx`           | Deck B FX bank selected                            |
|`on_right_sampler`      | Deck B SAMPLER bank selected                       |
|`on_left_sync_off`      | Deck A SYNC OFF button (SHIFT + SYNC)              |
|`on_left_prev_track`    | Deck A Previous Track button (SHIFT + CUE)         |
|`on_left_stutter`       | Deck A STUTTER button (SHIFT + PLAY)               |
|`on_cue_master`         | CUE MASTER button (SHIFT + LEFT HEADPHONES)        |
|`on_right_sync_off`     | Deck B SYNC OFF button (SHIFT + SYNC)              |
|`on_right_prev_track`   | Deck B Previous Track button (SHIFT + CUE)         |
|`on_right_stutter`      | Deck B STUTTER button (SHIFT + PLAY)               |
|`on_cue_mix`            | CUE + MIX button (SHIFT + RIGHT HEADPHONES)        |
|`on_left_hot_cue_1`     | Deck A HOT CUE pad 1 button                        |
|`on_left_hot_cue_2`     | Deck A HOT CUE pad 2 button                        |
|`on_left_hot_cue_3`     | Deck A HOT CUE pad 3 button                        |
|`on_left_hot_cue_4`     | Deck A HOT CUE pad 4 button                        |
|`on_left_loop_1`        | Deck A LOOP pad 1 button                           |
|`on_left_loop_2`        | Deck A LOOP pad 2 button                           |
|`on_left_loop_3`        | Deck A LOOP pad 3 button                           |
|`on_left_loop_4`        | Deck A LOOP pad 4 button                           |
|`on_left_fx_1`          | Deck A FX pad 1 button                             |
|`on_left_fx_2`          | Deck A FX pad 2 button                             |
|`on_left_fx_3`          | Deck A FX pad 3 button                             |
|`on_left_fx_4`          | Deck A FX pad 4 button                             |
|`on_left_sampler_1`     | Deck A SAMPLER pad 1 button                        |
|`on_left_sampler_2`     | Deck A SAMPLER pad 2 button                        |
|`on_left_sampler_3`     | Deck A SAMPLER pad 3 button                        |
|`on_left_sampler_4`     | Deck A SAMPLER pad 4 button                        |
|`on_right_hot_cue_1`    | Deck B HOT CUE pad 1 button                        |
|`on_right_hot_cue_2`    | Deck B HOT CUE pad 2 button                        |
|`on_right_hot_cue_3`    | Deck B HOT CUE pad 3 button                        |
|`on_right_hot_cue_4`    | Deck B HOT CUE pad 4 button                        |
|`on_right_loop_1`       | Deck B LOOP pad 1 button                           |
|`on_right_loop_2`       | Deck B LOOP pad 2 button                           |
|`on_right_loop_3`       | Deck B LOOP pad 3 button                           |
|`on_right_loop_4`       | Deck B LOOP pad 4 button                           |
|`on_right_fx_1`         | Deck B FX pad 1 button                             |
|`on_right_fx_2`         | Deck B FX pad 2 button                             |
|`on_right_fx_3`         | Deck B FX pad 3 button                             |
|`on_right_fx_4`         | Deck B FX pad 4 button                             |
|`on_right_sampler_1`    | Deck B SAMPLER pad 1 button                        |
|`on_right_sampler_2`    | Deck B SAMPLER pad 2 button                        |
|`on_right_sampler_3`    | Deck B SAMPLER pad 3 button                        |
|`on_right_sampler_4`    | Deck B SAMPLER pad 4 button                        |


### `control-change` events

Sent when value changes. Methods with a single argument, `value`, of type `int`, that corresponds with the computed value of the generated events.

| Method name              | Control element                                    |
|--------------------------|----------------------------------------------------|
|`on_crossfader_slide`     | Crossfader position, in range [0, 16256]           |
|`on_master_gain`          | Master volume pot, in range [0, 16256]             |
|`on_headphones_gain`      | Headphones volume pot, in range [0, 16256]         |
|`on_left_volume`          | Deck A volume pot, in range [0, 16256]             |
|`on_left_bass_filter`     | Deck A bass/filter pot, in range [0, 16256]        |
|`on_left_tempo_slide`     | Deck A tempo slider, in range [0, 16256]           |
|`on_left_wheel_transport` | Deck A jog wheel transport, CW = 1, CCW = 127      |
|`on_left_wheel_scratch`   | Deck A jog wheel scratch, CW = 1, CCW = 127        |
|`on_right_volume`         | Deck B volume pot, in range [0, 16256]             |
|`on_right_bass_filter`    | Deck B bass/filter pot, in range [0, 16256]        |
|`on_right_tempo_slide`    | Deck B tempo slider, in range [0, 16256]           |
|`on_right_wheel_transport`| Deck B jog wheel transport, CW = 1, CCW = 127      |
|`on_right_wheel_scratch`  | Deck B jog wheel scratch, CW = 1, CCW = 127        |


## LED names

These are the constants that can be used to control the LEDs, using functions like `led_on()`, `led_off()`, `set_led()` or `led_blink()`.

| LED name            | Control LED element                                |
|---------------------|----------------------------------------------------|
|`VINYL`              | Vinyl button LED                                   |
|`LEFT_SYNC`          | Deck A SYNC button LED                             |
|`LEFT_CUE`           | Deck A CUE button LED                              |
|`LEFT_PLAY`          | Deck A PLAY button LED                             |
|`LEFT_HEADPHONES`    | Deck A Headphones button LED                       |
|`LEFT_HOT_CUE_1`     | Deck A HOT CUE pad 1 button LED                    |
|`LEFT_HOT_CUE_2`     | Deck A HOT CUE pad 2 button LED                    |
|`LEFT_HOT_CUE_3`     | Deck A HOT CUE pad 3 button LED                    |
|`LEFT_HOT_CUE_4`     | Deck A HOT CUE pad 4 button LED                    |
|`LEFT_LOOP_1`        | Deck A LOOP pad 1 button LED                       |
|`LEFT_LOOP_2`        | Deck A LOOP pad 2 button LED                       |
|`LEFT_LOOP_3`        | Deck A LOOP pad 3 button LED                       |
|`LEFT_LOOP_4`        | Deck A LOOP pad 4 button LED                       |
|`LEFT_FX_1`          | Deck A FX pad 1 button LED                         |
|`LEFT_FX_2`          | Deck A FX pad 2 button LED                         |
|`LEFT_FX_3`          | Deck A FX pad 3 button LED                         |
|`LEFT_FX_4`          | Deck A FX pad 4 button LED                         |
|`LEFT_SAMPLER_1`     | Deck A SAMPLER pad 1 button LED                    |
|`LEFT_SAMPLER_2`     | Deck A SAMPLER pad 2 button LED                    |
|`LEFT_SAMPLER_3`     | Deck A SAMPLER pad 3 button LED                    |
|`LEFT_SAMPLER_4`     | Deck A SAMPLER pad 4 button LED                    |
|`RIGHT_SYNC`         | Deck B SYNC button LED                             |
|`RIGHT_CUE`          | Deck B CUE button LED                              |
|`RIGHT_PLAY`         | Deck B PLAY button LED                             |
|`RIGHT_HEADPHONES`   | Deck B Headphones button LED                       |
|`RIGHT_HOT_CUE_1`    | Deck B HOT CUE pad 1 button LED                    |
|`RIGHT_HOT_CUE_2`    | Deck B HOT CUE pad 2 button LED                    |
|`RIGHT_HOT_CUE_3`    | Deck B HOT CUE pad 3 button LED                    |
|`RIGHT_HOT_CUE_4`    | Deck B HOT CUE pad 4 button LED                    |
|`RIGHT_LOOP_1`       | Deck B LOOP pad 1 button LED                       |
|`RIGHT_LOOP_2`       | Deck B LOOP pad 2 button LED                       |
|`RIGHT_LOOP_3`       | Deck B LOOP pad 3 button LED                       |
|`RIGHT_LOOP_4`       | Deck B LOOP pad 4 button LED                       |
|`RIGHT_FX_1`         | Deck B FX pad 1 button LED                         |
|`RIGHT_FX_2`         | Deck B FX pad 2 button LED                         |
|`RIGHT_FX_3`         | Deck B FX pad 3 button LED                         |
|`RIGHT_FX_4`         | Deck B FX pad 4 button LED                         |
|`RIGHT_SAMPLER_1`    | Deck B SAMPLER pad 1 button LED                    |
|`RIGHT_SAMPLER_2`    | Deck B SAMPLER pad 2 button LED                    |
|`RIGHT_SAMPLER_3`    | Deck B SAMPLER pad 3 button LED                    |
|`RIGHT_SAMPLER_4`    | Deck B SAMPLER pad 4 button LED                    |

## BANK names

The DJControl has 4 banks of pads for each deck. These are the names used to change them. Used with the method `change_bank`. Note that you can also change bank using the DJControl buttons, these are for switching using your software.

| BANK name           | Bank activated                                     |
|---------------------|----------------------------------------------------|
|`LEFT_MODE_HOT_CUE`  | Deck A HOT CUE bank                                |
|`LEFT_MODE_LOOP`     | Deck A LOOP bank                                   |
|`LEFT_MODE_FX`       | Deck A FX bank                                     |
|`LEFT_MODE_SAMPLER`  | Deck A SAMPLER bank                                |
|`RIGHT_MODE_HOT_CUE` | Deck B HOT CUE bank                                |
|`RIGHT_MODE_LOOP`    | Deck B LOOP bank                                   |
|`RIGHT_MODE_FX`      | Deck B FX bank                                     |
|`RIGHT_MODE_SAMPLER` | Deck B SAMPLER bank                                |

