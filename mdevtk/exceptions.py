# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

class MDevTKException(RuntimeError):
    pass


class NoDeviceFound(MDevTKException):
    def __init__(self, name):
        super().__init__(f"No device ({name}) found!")
