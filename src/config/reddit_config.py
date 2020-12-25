import os
import string
import datetime
from logs.logger import log

AUTH = {
  # app creds
  "client_id":"",
  "client_secret":"",
  # reddit account creds
  "username":"",
  "password":"",
}

for config in list(AUTH):
  config_envar = f"REDDIT_BOT_{config}".upper()
  if os.environ.get(config_envar):
    log.info(f"loading {config_envar} from envar")
    AUTH[config]=os.environ.get(config_envar)
  else:
    log.info(f"no environment config for: {config_envar}")

log.info(AUTH)

CONFIG = {
  "chances": {
  "post": 0.05,
  }
}

