from apis import reddit_api
from config import reddit_config
from utils import chance
from bots.reddit.actions.post_actions import Posts
from bots.reddit.actions.comments.comment_actions import Comments
from bots.reddit.actions.cleanup_actions import Cleanup
from logs.logger import log
import time, sys

class RedditBot():
  def __init__(self, config=reddit_config.CONFIG):
    self.api = reddit_api
    self.ready = False
    self.posts = Posts()
    self.comments = Comments()
    self.cleanup = Cleanup()
    self.config = config

  def _init(self):
    user = self.api.user.me()
    if user == None:
      log.info("User auth failed, Reddit bot shutting down")
      sys.exit()
    else:
      log.info(f"running as user: {user}")
      self.ready = True

  def run(self):
    if self.ready:
      # log.info("running reddit bot")
      self.posts.repost(roll=self.config['reddit_post_chance'])
      self.comments.comment(roll=self.config['reddit_comment_chance'])
      self.cleanup.remove_low_scores(roll=self.config['reddit_remove_low_scores'])
    else:
      self._init()
      self.run()
      # log.info("not running reddit bot - not ready")



