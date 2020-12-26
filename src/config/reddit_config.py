import os
import string
import datetime
from utils import prefer_envar
from logs.logger import log

AUTH = prefer_envar({
  # app creds
  "reddit_client_id":"",
  "reddit_client_secret":"",
  # reddit account creds
  "reddit_username":"",
  "reddit_password":"",
})

log.info(AUTH)

CONFIG = prefer_envar({
  "reddit_post_chance": 0.05,
})

log.info(CONFIG)
