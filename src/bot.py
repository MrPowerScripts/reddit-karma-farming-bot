from bots.reddit import RedditBot
from utils import countdown

reddit = RedditBot()

def run():
  while True:
    reddit.run()
    countdown(1)
