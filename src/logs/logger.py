#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
import os
from logs.log_utils import NewLineFileHandler, NewLineStreamHandler


file_log_format = logging.Formatter("%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s")
stream_log_format = logging.Formatter("%(asctime)s %(message)s", "%H:%M:%S")
logFile = "info.log"

file_handler = RotatingFileHandler(logFile, mode="a", maxBytes=15 * 1024 * 1024, backupCount=2, encoding=None, delay=0)
file_handler.setFormatter(file_log_format)

stream_handler =  logging.StreamHandler()
stream_handler.setFormatter(stream_log_format)

log = logging.getLogger(__name__)

if "DEBUG" in os.environ:
    log.setLevel(logging.DEBUG)
    print("debug logging")
else:
    log.setLevel(logging.INFO)
    print("info loggin")

log.addHandler(stream_handler)
log.addHandler(file_handler)
