from tinydb import TinyDB, Query
from tinydb.operations import delete
from utils import BASE_DIR, MAIN_DB, bytesto
from logger import log
import os
import time

db = TinyDB('{}/db.json'.format(BASE_DIR))

db_dates = db.table('dates')
db_common = db.table('common')
Dates = Query()
Common = Query()

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
