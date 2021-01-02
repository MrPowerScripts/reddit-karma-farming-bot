from apis import reddit_api
from config import reddit_config
from utils import chance
from bots.reddit.actions.post_actions import Posts
from bots.reddit.actions.comments.comment_actions import Comments
from bots.reddit.actions.cleanup_actions import Cleanup
from logs.logger import log
import time, sys
from collections import namedtuple
from .utils import should_we_sleep

BotAction = namedtuple("BotAction", 'name call')

class RedditBot():
  def __init__(self, config=reddit_config.CONFIG):
    self.api = reddit_api
    self.ready = False
    self.config = config
    self.posts = Posts()
    self.comments = Comments()
    self.cleanup = Cleanup()
    self.actions = [
      BotAction('reddit_post_chance', self.posts.repost),
      BotAction('reddit_comment_chance', self.comments.comment),
      BotAction('reddit_shadowban_check', self.cleanup.shadow_check),
      BotAction('reddit_remove_low_scores', self.cleanup.remove_low_scores),
    ]

  def _init(self):
    # check if account is set
    user = self.api.user.me()
    if user == None:
      log.info("User auth failed, Reddit bot shutting down")
      sys.exit()
    else:
      log.info(f"running as user: {user}")
      self.ready = True
    # check if account is shadowbanned
    self.cleanup.shadow_check()
    log.info("The bot is now running. It has a chance to perform an action every second. Be patient")

  def tick(self):
    if not should_we_sleep():
      for action in self.actions:
        if chance(self.config[action.name]):
          log.info(f"running action: {action.name}")
          action.call()

  def run(self):
    if self.ready:
      self.tick()
    else:
      self._init()
      self.run()
      # log.info("not running reddit bot - not ready")



