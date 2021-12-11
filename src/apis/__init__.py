#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from config import reddit_config
from .reddit import RedditAPI
from .pushshift import PS

reddit_api = RedditAPI(**reddit_config.AUTH).api

pushshift_api = PS()