#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import random
import datetime
import os
import functools
import socket
import collections
import argparse
from requests import get
from os.path import expanduser
from logger import log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "brains")
MAIN_DB = os.path.join(BASE_DIR, "brains/brain.db")
MAIN_DB_MIN_SIZE = "50mb"
MAIN_DB_MAX_SIZE = "300mb"
#MAIN_DB = DB_DIR + "/brain.db"
SCORE_THRESHOLD = 0  # downvote
TOP_SUBREDDIT_NUM = 10  # number of subreddits to search for repost-able content
MIN_SCORE = 0  # for posts to repost
SUBMISSION_SEARCH_TEMPLATE = "https://api.pushshift.io/reddit/search/submission/?after={after}&before={before}&sort_type=score&sort=desc&subreddit={subreddit}"
DAY = 86400  # POSIX day (exact value)
MINUTE = 60
PROBABILITIES = {"REPLY": 0.02, "SUBMISSION": 0.005, "SHADOWCHECK": 0.002, "LEARN": 0.02, "DELETE": 0.02}
MAX_CACHE_SIZE = 128
NUMBER_DAYS_FOR_POST_TO_BE_OLD = 365
SUBREDDIT_LIST = [] # limit learning and posting to these subreddits. Empty = Random
DISALLOWED_WORDS_FILENAME = os.path.join(BASE_DIR, "disallowed_words.txt")
DISALLOWED_SUBS_FILENAME = os.path.join(BASE_DIR, "disallowed_subs.txt")
# Logging options
LOG_LEARNED_COMMENTS = False
SHOW_SLEEP_LOGGING = True

# array of tuples with time windows. 
# bot will run if current utc time in between listed values
# provide a list of tuples, with a two sub tuples
# the sub tuples should be a start time, annd stop time
# using (hours, minutes) as a 24h clock
USE_SLEEP_SCHEDULE = False
BOT_SCHEDULES = [
  ((4,00),(5,00)),
  ((9,30),(23,20)),
  ]

SCHEDULES = []
for schedule in BOT_SCHEDULES:
  SCHEDULES.append(((datetime.time(schedule[0][0], schedule[0][1])), (datetime.time(schedule[1][0], schedule[1][1]))))

BOT_SCHEDULES = SCHEDULES

subreddit = collections.namedtuple(
    "Subreddit", ["name", "rank", "url", "subscribers", "type"]
)

reddit_bot_action = collections.namedtuple(
    "RedditBotAction", ["name", "action", "probability", "rate_limit_unlock_epoch"]
)


DISALLOWED_WORDS = []

with open(DISALLOWED_WORDS_FILENAME, "r") as disallowed_words_obj:
    for line in disallowed_words_obj:
        DISALLOWED_WORDS.append(line.lower().strip())

DISALLOWED_SUBS = []

with open(DISALLOWED_SUBS_FILENAME, "r") as disallowed_subs_obj:
    for line in disallowed_subs_obj:
        DISALLOWED_SUBS.append(line.lower().strip())

def get_args():
  parser = argparse.ArgumentParser(description='The bot needs stuff')
  parser.add_argument('-u','--username', default=os.environ.get('REDDIT_USERNAME'))
  parser.add_argument('-p','--password', default=os.environ.get('REDDIT_PASSWORD'))
  parser.add_argument('-c','--clientid', default=os.environ.get('REDDIT_CLIENT_ID'))
  parser.add_argument('-s','--secret', default=os.environ.get('REDDIT_SECRET'))
  parser.add_argument('-a','--useragent', default=os.environ.get('REDDIT_USER_AGENT'))
  parser.add_argument('-l','--sublist', default=os.environ.get('REDDIT_SUBREDDITS'))
  return  parser.parse_args()

if get_args().sublist: # Prefer subreddit list from envars
  SUBREDDIT_LIST = get_args().sublist.strip().split(",")
  log.info("Getting subreddit list from envar or args")
else:
  log.info('Using subreddit list from utils.py')

log.info(SUBREDDIT_LIST)

def get_current_epoch():
    return int(time.time())

def convert_size_to_bytes(size_str):
    """Convert human filesizes to bytes.
    https://stackoverflow.com/questions/44307480/convert-size-notation-with-units-100kb-32mb-to-number-of-bytes-in-python
    Special cases:
     - singular units, e.g., "1 byte"
     - byte vs b
     - yottabytes, zetabytes, etc.
     - with & without spaces between & around units.
     - floats ("5.2 mb")

    To reverse this, see hurry.filesize or the Django filesizeformat template
    filter.

    :param size_str: A human-readable string representing a file size, e.g.,
    "22 megabytes".
    :return: The number of bytes represented by the string.
    """
    multipliers = {
        'kilobyte':  1024,
        'megabyte':  1024 ** 2,
        'gigabyte':  1024 ** 3,
        'terabyte':  1024 ** 4,
        'petabyte':  1024 ** 5,
        'exabyte':   1024 ** 6,
        'zetabyte':  1024 ** 7,
        'yottabyte': 1024 ** 8,
        'kb': 1024,
        'mb': 1024**2,
        'gb': 1024**3,
        'tb': 1024**4,
        'pb': 1024**5,
        'eb': 1024**6,
        'zb': 1024**7,
        'yb': 1024**8,
    }

    for suffix in multipliers:
        size_str = size_str.lower().strip().strip('s')
        if size_str.lower().endswith(suffix):
            return int(float(size_str[0:-len(suffix)]) * multipliers[suffix])
    else:
        if size_str.endswith('b'):
            size_str = size_str[0:-1]
        elif size_str.endswith('byte'):
            size_str = size_str[0:-4]
    return int(size_str)

MAIN_DB_MIN_SIZE = convert_size_to_bytes(MAIN_DB_MIN_SIZE)  # in bytes
MAIN_DB_MAX_SIZE = convert_size_to_bytes(MAIN_DB_MAX_SIZE)  # in bytes

def check_internet(host="1.1.1.1", port=53, timeout=5):
    """
    Host: 1.1.1.1 (cloudflare DNS)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        log.error(ex.message)
        return False


def get_seconds_to_wait(ex_msg=None):
    try:
        msg = ex_msg.lower()
        search = re.search(r"\b(minutes)\b", msg)
        # I found out that if the message said 3 minute
        # it could be 3 minute 20 seconds, so to be safe and avoid another exception,
        # we wait a full extra minute
        minutes = int(msg[search.start() - 2]) + 1
        return minutes * 60
    except:
        return 60


def get_public_ip():
    try:
        for service in ["https://api.ipify.org", "http://ip.42.pl/raw"]:
            external_ip = get(service).text
            if external_ip:
                return external_ip
    except Exception as e:
        # try one more before giving up
        try:
            return get("http://httpbin.org/ip").json()["origin"].split(",")[0]
        except:
            log.error("could not check external ip")


# Python <3.2 does not have lru_cache built in
# only backport packages exist which are pretty old
# and have too much bloat
# https://stackoverflow.com/a/18723434/5682956
def lru_cache(maxsize=255, timeout=None):
    """lru_cache(maxsize = 255, timeout = None) --> returns a decorator which returns an instance (a descriptor).

        Purpose         - This decorator factory will wrap a function / instance method and will supply a caching mechanism to the function.
                            For every given input params it will store the result in a queue of maxsize size, and will return a cached ret_val
                            if the same parameters are passed.

        Params          - maxsize - int, the cache size limit, anything added above that will delete the first values enterred (FIFO).
                            This size is per instance, thus 1000 instances with maxsize of 255, will contain at max 255K elements.
                        - timeout - int / float / None, every n seconds the cache is deleted, regardless of usage. If None - cache will never be refreshed.

        Notes           - If an instance method is wrapped, each instance will have it's own cache and it's own timeout.
                        - The wrapped function will have a cache_clear variable inserted into it and may be called to clear it's specific cache.
                        - The wrapped function will maintain the original function's docstring and name (wraps)
                        - The type of the wrapped function will no longer be that of a function but either an instance of _LRU_Cache_class or a functool.partial type.

        On Error        - No error handling is done, in case an exception is raised - it will permeate up.
    """

    class _LRU_Cache_class(object):
        def __init__(self, input_func, max_size, timeout):
            self._input_func = input_func
            self._max_size = max_size
            self._timeout = timeout

            # This will store the cache for this function, format - {caller1 : [OrderedDict1, last_refresh_time1], caller2 : [OrderedDict2, last_refresh_time2]}.
            #   In case of an instance method - the caller is the instance, in case called from a regular function - the caller is None.
            self._caches_dict = {}

        def cache_clear(self, caller=None):
            # Remove the cache for the caller, only if exists:
            if caller in self._caches_dict:
                del self._caches_dict[caller]
                self._caches_dict[caller] = [collections.OrderedDict(), time.time()]

        def __get__(self, obj, objtype):
            """ Called for instance methods """
            return_func = functools.partial(self._cache_wrapper, obj)
            return_func.cache_clear = functools.partial(self.cache_clear, obj)
            # Return the wrapped function and wraps it to maintain the docstring and the name of the original function:
            return functools.wraps(self._input_func)(return_func)

        def __call__(self, *args, **kwargs):
            """ Called for regular functions """
            return self._cache_wrapper(None, *args, **kwargs)

        # Set the cache_clear function in the __call__ operator:
        __call__.cache_clear = cache_clear

        def _cache_wrapper(self, caller, *args, **kwargs):
            # Create a unique key including the types (in order to differentiate between 1 and '1'):
            kwargs_key = "".join(
                map(
                    lambda x: str(x) + str(type(kwargs[x])) + str(kwargs[x]),
                    sorted(kwargs),
                )
            )
            key = "".join(map(lambda x: str(type(x)) + str(x), args)) + kwargs_key

            # Check if caller exists, if not create one:
            if caller not in self._caches_dict:
                self._caches_dict[caller] = [collections.OrderedDict(), time.time()]
            else:
                # Validate in case the refresh time has passed:
                if self._timeout != None:
                    if time.time() - self._caches_dict[caller][1] > self._timeout:
                        self.cache_clear(caller)

            # Check if the key exists, if so - return it:
            cur_caller_cache_dict = self._caches_dict[caller][0]
            if key in cur_caller_cache_dict:
                return cur_caller_cache_dict[key]

            # Validate we didn't exceed the max_size:
            if len(cur_caller_cache_dict) >= self._max_size:
                # Delete the first item in the dict:
                cur_caller_cache_dict.popitem(False)

            # Call the function and store the data in the cache (call it with the caller in case it's an instance function - Ternary condition):
            cur_caller_cache_dict[key] = (
                self._input_func(caller, *args, **kwargs)
                if caller != None
                else self._input_func(*args, **kwargs)
            )
            return cur_caller_cache_dict[key]

    # Return the decorator wrapping the class (also wraps the instance to maintain the docstring and the name of the original function):
    return lambda input_func: functools.wraps(input_func)(
        _LRU_Cache_class(input_func, maxsize, timeout)
    )


def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
      sample code:
          print('mb= ' + str(bytesto(314575262000000, 'm')))
      sample output:
          mb= 300002347.946
  """

    a = {"k": 1, "m": 2, "g": 3, "t": 4, "p": 5, "e": 6}
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return r


def is_past_one_day(time_to_compare):
    return int(time.time()) - time_to_compare >= DAY


def countdown(seconds):
    log.info("sleeping: " + str(seconds) + " seconds")
    for i in range(seconds, 0, -1):
        print("\x1b[2K\r" + str(i) + " ")
        time.sleep(1)
    log.info("waking up")


def prob(probability):
    rando = random.random()
    log.info("prob: " + str(probability) + " rolled: " + str(rando))
    return rando < probability


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def should_we_sleep():
    
    CHECKS = []
    for schedule in BOT_SCHEDULES:
      print(schedule[0], schedule[1])
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
