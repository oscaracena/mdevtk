# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from ..controller import DeviceController


class DJControlStarlight(DeviceController):
    # 2-control pots/sliders' max value
    MAX_VALUE            = 128 * 127

    # Control commands
    CMD_LED_ON           = 0x7f
    CMD_LED_OFF          = 0x00
    CMD_CHANGE_BANK      = 0x7f

    # LED ids: (channel, note)
    VINYL                = (2, 3)

    LEFT_SYNC            = (1, 5)
    LEFT_CUE             = (1, 6)
    LEFT_PLAY            = (1, 7)
    LEFT_HEADPHONES      = (1, 12)
    LEFT_HOT_CUE_1       = (6, 0)
    LEFT_HOT_CUE_2       = (6, 1)
    LEFT_HOT_CUE_3       = (6, 2)
    LEFT_HOT_CUE_4       = (6, 3)
    LEFT_LOOP_1          = (6, 16)
    LEFT_LOOP_2          = (6, 17)
    LEFT_LOOP_3          = (6, 18)
    LEFT_LOOP_4          = (6, 19)
    LEFT_FX_1            = (6, 32)
    LEFT_FX_2            = (6, 33)
    LEFT_FX_3            = (6, 34)
    LEFT_FX_4            = (6, 35)
    LEFT_SAMPLER_1       = (6, 48)
    LEFT_SAMPLER_2       = (6, 49)
    LEFT_SAMPLER_3       = (6, 50)
    LEFT_SAMPLER_4       = (6, 51)

    RIGHT_SYNC           = (2, 5)
    RIGHT_CUE            = (2, 6)
    RIGHT_PLAY           = (2, 7)
    RIGHT_HEADPHONES     = (2, 12)
    RIGHT_HOT_CUE_1      = (7, 0)
    RIGHT_HOT_CUE_2      = (7, 1)
    RIGHT_HOT_CUE_3      = (7, 2)
    RIGHT_HOT_CUE_4      = (7, 3)
    RIGHT_LOOP_1         = (7, 16)
    RIGHT_LOOP_2         = (7, 17)
    RIGHT_LOOP_3         = (7, 18)
    RIGHT_LOOP_4         = (7, 19)
    RIGHT_FX_1           = (7, 32)
    RIGHT_FX_2           = (7, 33)
    RIGHT_FX_3           = (7, 34)
    RIGHT_FX_4           = (7, 35)
    RIGHT_SAMPLER_1      = (7, 48)
    RIGHT_SAMPLER_2      = (7, 49)
    RIGHT_SAMPLER_3      = (7, 50)
    RIGHT_SAMPLER_4      = (7, 51)

    LEFT_BASE            = (1, 35)
    RIGHT_BASE           = (2, 35)
    BASE_OFF             = (0, 36)

    # MODE controls
    LEFT_MODE_HOT_CUE    = (1, 15)
    LEFT_MODE_LOOP       = (1, 16)
    LEFT_MODE_FX         = (1, 17)
    LEFT_MODE_SAMPLER    = (1, 18)

    RIGHT_MODE_HOT_CUE   = (2, 15)
    RIGHT_MODE_LOOP      = (2, 16)
    RIGHT_MODE_FX        = (2, 17)
    RIGHT_MODE_SAMPLER   = (2, 18)

    # TOGGLE controls
    TOGGLE_BASS_FILTER   = (0, 1)

    def __init__(self):
        super().__init__("DJControl Starlight")

        self.on_note(channel=0, note=1,  cb="on_bass_filter_toggle"),
        self.on_note(channel=0, note=3,  cb="on_shift"),

        self.on_note(channel=1, note=5,  cb="on_left_sync"),
        self.on_note(channel=1, note=6,  cb="on_left_cue"),
        self.on_note(channel=1, note=7,  cb="on_left_play"),
        self.on_note(channel=1, note=8,  cb="on_left_wheel_touch"),
        self.on_note(channel=1, note=12, cb="on_left_headphones"),
        self.on_note(channel=1, note=15, cb="on_left_hot_cue"),
        self.on_note(channel=1, note=16, cb="on_left_loop"),
        self.on_note(channel=1, note=17, cb="on_left_fx"),
        self.on_note(channel=1, note=18, cb="on_left_sampler"),

        self.on_note(channel=2, note=3,  cb="on_vinyl"),
        self.on_note(channel=2, note=5,  cb="on_right_sync"),
        self.on_note(channel=2, note=6,  cb="on_right_cue"),
        self.on_note(channel=2, note=7,  cb="on_right_play"),
        self.on_note(channel=2, note=8,  cb="on_right_wheel_touch"),
        self.on_note(channel=2, note=12, cb="on_right_headphones"),
        self.on_note(channel=2, note=15, cb="on_right_hot_cue"),
        self.on_note(channel=2, note=16, cb="on_right_loop"),
        self.on_note(channel=2, note=17, cb="on_right_fx"),
        self.on_note(channel=2, note=18, cb="on_right_sampler"),

        self.on_note(channel=4, note=5,  cb="on_left_sync_off"),
        self.on_note(channel=4, note=6,  cb="on_left_prev_track"),
        self.on_note(channel=4, note=7,  cb="on_left_stutter"),
        self.on_note(channel=4, note=12, cb="on_cue_master"),

        self.on_note(channel=5, note=5,  cb="on_right_sync_off"),
        self.on_note(channel=5, note=6,  cb="on_right_prev_track"),
        self.on_note(channel=5, note=7,  cb="on_right_stutter"),
        self.on_note(channel=5, note=12, cb="on_cue_mix"),

        self.on_note(channel=6, note=0,  cb="on_left_hot_cue_1"),
        self.on_note(channel=6, note=1,  cb="on_left_hot_cue_2"),
        self.on_note(channel=6, note=2,  cb="on_left_hot_cue_3"),
        self.on_note(channel=6, note=3,  cb="on_left_hot_cue_4"),
        self.on_note(channel=6, note=16, cb="on_left_loop_1"),
        self.on_note(channel=6, note=17, cb="on_left_loop_2"),
        self.on_note(channel=6, note=18, cb="on_left_loop_3"),
        self.on_note(channel=6, note=19, cb="on_left_loop_4"),
        self.on_note(channel=6, note=32, cb="on_left_fx_1"),
        self.on_note(channel=6, note=33, cb="on_left_fx_2"),
        self.on_note(channel=6, note=34, cb="on_left_fx_3"),
        self.on_note(channel=6, note=35, cb="on_left_fx_4"),
        self.on_note(channel=6, note=48, cb="on_left_sampler_1"),
        self.on_note(channel=6, note=49, cb="on_left_sampler_2"),
        self.on_note(channel=6, note=50, cb="on_left_sampler_3"),
        self.on_note(channel=6, note=51, cb="on_left_sampler_4"),

        self.on_note(channel=7, note=0,  cb="on_right_hot_cue_1"),
        self.on_note(channel=7, note=1,  cb="on_right_hot_cue_2"),
        self.on_note(channel=7, note=2,  cb="on_right_hot_cue_3"),
        self.on_note(channel=7, note=3,  cb="on_right_hot_cue_4"),
        self.on_note(channel=7, note=16, cb="on_right_loop_1"),
        self.on_note(channel=7, note=17, cb="on_right_loop_2"),
        self.on_note(channel=7, note=18, cb="on_right_loop_3"),
        self.on_note(channel=7, note=19, cb="on_right_loop_4"),
        self.on_note(channel=7, note=32, cb="on_right_fx_1"),
        self.on_note(channel=7, note=33, cb="on_right_fx_2"),
        self.on_note(channel=7, note=34, cb="on_right_fx_3"),
        self.on_note(channel=7, note=35, cb="on_right_fx_4"),
        self.on_note(channel=7, note=48, cb="on_right_sampler_1"),
        self.on_note(channel=7, note=49, cb="on_right_sampler_2"),
        self.on_note(channel=7, note=50, cb="on_right_sampler_3"),
        self.on_note(channel=7, note=51, cb="on_right_sampler_4"),

        # NOTE: CC 'controls' are ordered in little-endian mode (LSB, MSB)
        self.on_cc(channel=0, controls=(32, 0), cb="on_crossfader_slide")
        self.on_cc(channel=0, controls=(35, 3), cb="on_master_gain")
        self.on_cc(channel=0, controls=(36, 4), cb="on_headphones_gain")

        self.on_cc(channel=1, controls=(32, 0), cb="on_left_volume")
        self.on_cc(channel=1, controls=(34, 2), cb="on_left_bass_filter")
        self.on_cc(channel=1, controls=(40, 8), cb="on_left_tempo_slide")
        self.on_cc(channel=1, controls=(9,),    cb="on_left_wheel_transport")
        self.on_cc(channel=1, controls=(10,),   cb="on_left_wheel_scratch")

        self.on_cc(channel=2, controls=(32, 0), cb="on_right_volume")
        self.on_cc(channel=2, controls=(34, 2), cb="on_right_bass_filter")
        self.on_cc(channel=2, controls=(40, 8), cb="on_right_tempo_slide")
        self.on_cc(channel=2, controls=(9,),    cb="on_right_wheel_transport")
        self.on_cc(channel=2, controls=(10,),   cb="on_right_wheel_scratch")
