import config.common as common
import os
import datetime

AUTH = {
  # app creds
  "client_id":"",
  "client_secret":"",
  # reddit account creds
  "username":"",
  "password":"",
}

PROBABILITIES = {
  "REPLY": 0.002,
  "POST": 0.05,
  "SHADOWCHECK": 0.002,
  "DBCHECK": 0.005,
  "KARMACHECK" : 0.005,
  "LEARN": 0.02,
  "DELETE": 0.02,
}
