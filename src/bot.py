#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from cobe.brain import Brain
from logger import log
from utils import MAIN_DB

log.info("Main database: {}".format(MAIN_DB))
base_brain = Brain(MAIN_DB)
