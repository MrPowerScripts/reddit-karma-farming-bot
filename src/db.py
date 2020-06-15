from tinydb import TinyDB, Query
import datetime
import json
from utils import (
                  BASE_DIR, 
                  MAIN_DB, 
                  bytesto, 
                  BOT_SCHEDULES, 
                  DAY, 
                  is_time_between,
                  SHOW_SLEEP_LOGGING
)
from logger import log
from reddit import api
import os
import time

db = TinyDB('{}/db.json'.format(BASE_DIR))

db_dates = db.table('dates')
db_common = db.table('common')
db_config = db.table('config')
Dates = Query()
Common = Query()
Config = Query()

def set_user_info():
  me_data = api.user.me()
  j = {k: v for k,v in me_data.__dict__.items() if k != '_reddit'}
  # log.info(j)
  db_config.upsert({"config": "user", "value": j}, Config.config == "user")

def get_user_info():
  return db_config.get(Config.config == "user")

def set_db_size():
  if os.path.isfile(MAIN_DB):
    size = os.path.getsize(MAIN_DB)
    db_common.insert({"data": "db_size", "value": size, "db_size_timestamp": int(time.time()), "timestamp": int(time.time())})
    hours_ago_24 = int((int(time.time()) - 86400))
    db_common.remove(Common.db_size_timestamp < hours_ago_24)
  else:
    log.info('no database found in: {}'.format(MAIN_DB))

def get_db_size(human=False):
  if human:
    size = db_common.search(Common.data == "db_size")
    size = sorted(size, key=lambda k: k['db_size_timestamp'])
    return bytesto(size[-1].get("value") if size else 0, "m")
  else:
    size = db_common.search(Common.data == "db_size")
    return size[-1].get("value") if size else 0

def check_first_run():
  if not db_dates.search(Dates.first_run.exists()):
    log.info("This is the first bot run ever. Exciting!")
    db_dates.insert({"first_run": int(time.time())})
  else:
    log.info('not first run ever')


def should_we_sleep():
  
    best_schedule=[]

    first_run = [x for x in db_dates.all() if x == Dates.first_run][0]['first_run']
    # log.info("first run: {}".format(first_run))
    log.info('choosing schedule')
    sorted_schedules = sorted(BOT_SCHEDULES, key=lambda k: k['days'])
    for day in sorted_schedules:
      day_epoch = first_run + (int(day['days']) * DAY)
      current_epoch = int(time.time())
      if current_epoch > day_epoch:
        log.info("using schedule: {}".format(day))
        best_schedule=day['schedule']
        break

    CHECKS = []
    for schedule in best_schedule:
      if is_time_between(schedule[0], schedule[1]):
        if SHOW_SLEEP_LOGGING:
          log.info("sleep?: {} awake: {}, sleep: {}, current: {}".format(False, schedule[0], schedule[1], datetime.datetime.utcnow().time()))
        CHECKS.append(True)
      else:
        if SHOW_SLEEP_LOGGING:
          log.info("sleep?: {} awake: {}, sleep: {}, current: {}".format(True, schedule[0], schedule[1], datetime.datetime.utcnow().time()))
        CHECKS.append(False)
    
    # check if any of the time between checks returned true.
    # if there's a True in the list, it means we're between one of the scheduled times
    # and so this function returns False so the bot doesn't sleep
    log.info("check list: {}".format(CHECKS))
    if True in CHECKS:
      log.info("no need to sleep")
      return False
    else:
      log.info("it's sleepy time")
      return True