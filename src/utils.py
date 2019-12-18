#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import random
import os
import functools
import socket
import collections
from requests import get
from os.path import expanduser
from logger import log

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = expanduser("~")
DB_DIR = ROOT_DIR + "/brains"
MAIN_DB = DB_DIR + "/brain.db"
MAIN_DB_MIN_SIZE = 52428800  # in bytes
MAIN_DB_MAX_SIZE = 209715200  # in bytes
SCORE_THRESHOLD = -2  # downvote
TOP_SUBREDDIT_NUM = 10  # number of subreddits to search for repost-able content
MIN_SCORE = 30000  # for posts to repost
SUBMISSION_SEARCH_TEMPLATE = "https://api.pushshift.io/reddit/search/submission/?after={after}&before={before}&sort_type=score&sort=desc&subreddit={subreddit}"
DAY = 86400  # POSIX day (exact value)
MINUTE = 60
PROBABILITIES = {"REPLY": 0.02, "SUBMISSION": 0.02, "LEARN": 0.02, "DELETE": 0.02}
MAX_CACHE_SIZE = 128
NUMBER_DAYS_FOR_POST_TOBE_OLD = 365
SUBREDDIT_LIST = [] # limit learning and posting to these subreddits. Empty = Random

if os.environ.get("SUBREDDIT_LIST"): # Prefer subreddit list from envars
  SUBREDDIT_LIST = os.environ.get("SUBREDDIT_LIST").strip().split(",")
  log.info("Getting subreddit list from environment")
else:
  log.info('Getting subreddit list from utils.py')

log.info(SUBREDDIT_LIST)

subreddit = collections.namedtuple(
    "Subreddit", ["name", "rank", "url", "subscribers", "type"]
)

reddit_bot_action = collections.namedtuple(
    "RedditBotAction", ["name", "action", "probability", "rate_limit_unlock_epoch"]
)


def get_current_epoch():
    return int(time.time())


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
    for i in xrange(seconds, 0, -1):
        print("\x1b[2K\r" + str(i) + " ")
        time.sleep(1)
    log.info("waking up")


def prob(probability):
    rando = random.random()
    log.info("prob: " + str(probability) + "rand num: " + str(rando))
    return rando < probability
