# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2023, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

import logging


# Code from: https://stackoverflow.com/a/56944256/870503
class LoggingCustomFormatter(logging.Formatter):
    grey = "\x1b[90m"
    white = ""
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s:%(name)s:%(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: white + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_colour_logger(name):
    sh = logging.StreamHandler()
    sh.setFormatter(LoggingCustomFormatter())

    log = logging.getLogger(name)
    log.propagate = False
    log.addHandler(sh)
    return log


log = get_colour_logger("djcontrol")
