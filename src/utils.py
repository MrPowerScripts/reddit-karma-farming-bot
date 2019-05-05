import time
import random
import os
from collections import namedtuple
from os.path import expanduser
from logger import log

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = expanduser("~")
DB_DIR = "/reddit-karma-bot/brains"
MAIN_DB = DB_DIR + "/brain.db"
SCORE_THRESHOLD = -2
SUBMISSION_SEARCH_TEMPLATE = \
    "https://api.pushshift.io/reddit/submission/search/" \
    "?after={after}&before={before}" \
    "&sort_type=score&sort=desc" \
    "&subreddit={subreddit}"

subreddit = namedtuple("Subreddit", ["name", "rank", "url", "subscribers", "type"])


def bytesto(bytes, to, bsize=1024):
  """convert bytes to megabytes, etc.
      sample code:
          print('mb= ' + str(bytesto(314575262000000, 'm')))
      sample output: 
          mb= 300002347.946
  """

  a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
  r = float(bytes)
  for i in range(a[to]):
    r = r / bsize

  return(r)


def countdown(seconds):
  log.info('sleeping: ' + str(seconds) + " seconds")
  for i in xrange(seconds,0,-1):
      print('\x1b[2K\r' + str(i)+' ')
      time.sleep(1)
  log.info('waking up')


def prob(probability):
    rando = random.random() 
    log.info("prob: " + str(probability) + "rand num: " + str(rando))
    return rando < probability