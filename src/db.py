from tinydb import TinyDB, Query
from utils import BASE_DIR, MAIN_DB, bytesto
from logger import log
import os
import time

db = TinyDB('{}/db.json'.format(BASE_DIR))

db_dates = db.table('dates')
db_common = db.table('common')
dates = Query()

def set_db_size():
  if os.path.isfile(MAIN_DB):
    size = os.path.getsize(MAIN_DB)
    db_common.upsert({"config": "db_size", "value": size}, dates.config=="db_size")
  else:
    log.info('no database found in: {}'.format(MAIN_DB))

def get_db_size(human=False):
  if human:
    return bytesto(db_common.get(dates.config == "db_size").get('value'), "m")
  else:
    return db_common.get(dates.config == "db_size").get('value')

def check_first_run():
  if not db_dates.search(dates.first_run.exists()):
    log.info("This is the first bot run ever. Exciting!")
    db_dates.insert({"config": "first_run", "value": int(time.time())})
  else:
    log.info('not first run ever')
