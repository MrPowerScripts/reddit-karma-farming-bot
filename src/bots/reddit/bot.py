from apis.reddit import RedditAPI
from apis.pushshift import PushShift
from config import reddit
from utils import chance
import time

class RedditBot():
  def __init__(self):
    self.api = RedditAPI(**reddit.AUTH).api
    self.psapi = PushShift()
    self.ready = False

  def _init(self):
    print(f"running as user: {self.api.user.me()}")
    self.ready = True

  def run(self):
    if self.ready:
      # log.info("running reddit bot")
      self._repost()
    else:
      self._init()
      self.run()
      # log.info("not running reddit bot - not ready")

  def _repost(self, roll=reddit.PROBABILITIES["POST"]):
    if chance(roll):
      print("running _repost")
      # log.info("running _repost")
      subreddit = self.api.random_subreddit(nsfw=False)
      print(f"reposting to {subreddit.display_name}")
      post = self.api.submission(id=self.psapi.get_posts(subreddit.display_name)[0]['id'])
      print(post)

      if post.is_self:
        params = {"title": post.title, "selftext": post.selftext}
      else:
        params = {"title": post.title, "url": post.url}

      self.api.subreddit(subreddit.display_name).submit(**params)
    else:
      print("not running _repost")
      # log.info("not running _repost")

