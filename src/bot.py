from bots.reddit import RedditBot
from utils import countdown

def run():
  reddit = RedditBot()
  while True:
    reddit.run()
    countdown(1)
