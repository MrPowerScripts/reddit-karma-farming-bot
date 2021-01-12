import datetime
from logs.logger import log
from config.reddit_config import CONFIG
import time
from praw.models.redditors import Redditors

## USER UTILS

def parse_user(user: Redditors):
  i = {}
  i['comment_karma'] = user.comment_karma
  i['link_karma'] = user.link_karma
  i['username'] = user.name
  i['created_utc'] = user.created_utc
  i['created_utc_human'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(user.created_utc)) 
  return i

## SCHEDULE UTILS

EASY_SCHEDULES = {
  1: ((7,00),(10,00)),
  2: ((10,00),(14,00)),
  3: ((14,00),(18,00)),
  4: ((18,00),(22,00)),
  5: ((22,00),(2,00)),
}

# convert the easy schedules to the tuple values
BOT_SCHEDULE = [EASY_SCHEDULES.get(schedule) for schedule in CONFIG['reddit_sleep_schedule']]

log.info(f"using schedules: {BOT_SCHEDULE}")

# transform the schedule with datetime formatting
updated_schedules = [((datetime.time(schedule[0][0], schedule[0][1])), (datetime.time(schedule[1][0], schedule[1][1]))) for schedule in BOT_SCHEDULE]

BOT_SCHEDULE = updated_schedules


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def should_we_sleep():
    CHECKS = [True for schedule in BOT_SCHEDULE if is_time_between(schedule[0], schedule[1])]
    # check if any of the time between checks returned true.
    # if there's a True in the list, it means we're between one of the scheduled times
    # and so this function returns False so the bot doesn't sleep
    if True in CHECKS or not CONFIG.get('reddit_sleep_schedule'):
      # no need to sleep - the bot is within one of the time ranges
      return False
    else:
      log.info("it's sleepy time.. zzzzz :snore: zzzz")
      whats_left = []
      TIME_LEFT = [schedule[0] for schedule in BOT_SCHEDULE]
      for time_stamp in TIME_LEFT:
        # log.info(time_stamp)
        next_start = datetime.datetime.combine(datetime.date.today(), time_stamp)
        # log.info(f"next start: {next_start}")
        ts = int(next_start.timestamp())
        # if this goes negative then the next start is probably tomorrow
        if ts < int(time.time()):
          next_start = datetime.datetime.combine((datetime.date.today() + datetime.timedelta(days=1)), time_stamp)
          ts = next_start.timestamp()
          
        # collect all the seconds left for each time schedule to start
        # log.info(f"ts: {ts}")
        # log.info(f"time: {int(time.time())}")
        whats_left.append(ts - int(time.time()))
      
      #remove negative values and
      # get the shortest duration of time left before starting
      # log.info(whats_left)
      whats_left = [item for item in whats_left if item >= 0]

      # log.info(whats_left)
      time_left = int(min(whats_left))

      if time_left > 600:
        log.info(f"waking up in: {datetime.timedelta(seconds=time_left)} at {next_start}")
      
      sleep_time = int(time_left / 3)

      # have the bot sleep for a short while instead of tons of messages every second
      time.sleep(sleep_time)
      return True
