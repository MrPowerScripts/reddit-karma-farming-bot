#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s"
)

logFile = "info.log"

file_handler = RotatingFileHandler(
    logFile, mode="a", maxBytes=15 * 1024 * 1024, backupCount=2, encoding=None, delay=0
)
file_handler.setFormatter(log_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)

log = logging.getLogger(__name__)

if "DEBUG" in os.environ:
    log.setLevel(logging.DEBUG)
    print("debug logging")
else:
    log.setLevel(logging.INFO)
    print("info loggin")

log.addHandler(stream_handler)
log.addHandler(file_handler)
