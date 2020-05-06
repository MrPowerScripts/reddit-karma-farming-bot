from tinydb import TinyDB, Query
from utils import BASE_DIR
from logger import log
import time

db = TinyDB('{}/db.json'.format(BASE_DIR))

db_dates = db.table('dates')
dates = Query()


def check_first_run():
  if not db_dates.search(dates.first_run.exists()):
    log.info("This is the first bot run ever. Exciting!")
    db_dates.insert({"first_run": int(time.time())})
  else:
    log.info("This is the first bot run ever. Exciting!")
    log.info('bot first ran before')