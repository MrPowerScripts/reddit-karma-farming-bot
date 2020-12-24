import os
import string
import datetime

AUTH = {
  # app creds
  "client_id":"",
  "client_secret":"",
  # reddit account creds
  "username":"",
  "password":"",
}

for config in AUTH:
  # print(os.environ)
  if os.environ.get(f"BOT_{config}".upper()):
    # print(os.environ.get(f"BOT_{config}".upper()))
    AUTH[config]=os.environ.get(f"BOT_{config}".upper())

print(AUTH)

CONFIG = {
  "chances": {
  "post": 0.05,
  }
}

