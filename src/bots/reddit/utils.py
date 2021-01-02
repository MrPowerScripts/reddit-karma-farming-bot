import datetime
from logs.logger import log
from config.reddit_config import CONFIG
import time

BOT_SCHEDULE = []

EASY_SCHEDULES = {
  1: ((7,00),(10,00)),
  2: ((10,00),(14,00)),
  3: ((14,00),(18,00)),
  4: ((18,00),(22,00)),
  5: ((22,00),(2,00)),
}

# convert the easy schedules to the tuple values
for schedule in CONFIG['reddit_sleep_schedule']:
  BOT_SCHEDULE.append(EASY_SCHEDULES.get(schedule))

log.info(f"using schedules: {BOT_SCHEDULE}")

# transform the schedule with datetime formatting
updated_schedules = []
for schedule in BOT_SCHEDULE:
  # log.info(f"processing schedule: {schedule}")
  # log.info(schedule)
  bs1 = schedule[0][0]
  bs2 = schedule[0][1]
  bs3 = schedule[1][0]
  bs4 = schedule[1][1]
  # log.info(f"base schedules: {bs1}, {bs2} - {bs3}, {bs4}")
  updated_schedules.append(((datetime.time(bs1, bs2)), (datetime.time(bs3, bs4))))

BOT_SCHEDULE = updated_schedules


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def should_we_sleep():
    CHECKS = []
    TIME_LEFT = []
    for schedule in BOT_SCHEDULE:
      if is_time_between(schedule[0], schedule[1]):
        CHECKS.append(True)
      else:
        CHECKS.append(False)
        TIME_LEFT.append(schedule[0])
    # check if any of the time between checks returned true.
    # if there's a True in the list, it means we're between one of the scheduled times
    # and so this function returns False so the bot doesn't sleep
    if True in CHECKS:
      # no need to sleep - the bot is within one of the time ranges
      return False
    else:
      log.info("it's sleepy time.. zzzzz :snore: zzzz")
      whats_left = []
      # log.info(TIME_LEFT)
      for time_stamp in TIME_LEFT:
        next_start = datetime.datetime.combine(datetime.date.today(), time_stamp)
        ts = int(next_start.timestamp())
        # collect all the seconds left for each time schedule to start
        whats_left.append(ts - int(time.time()))
      
      #get the shortest duration of time left before starting
      time_left = min(whats_left)
      log.info(f"waking up in: {datetime.timedelta(seconds=time_left)} at {next_start}")
      sleep_time = time_left / 3
      # have the bot sleep for a short while instead of tons of messages every second
      time.sleep(sleep_time)
      return True