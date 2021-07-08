from apis import reddit_api
from config import reddit_config
from utils import chance
from bots.reddit.actions.post_actions import Posts
from bots.reddit.actions.comments.comment_actions import Comments
from bots.reddit.actions.cleanup_actions import Cleanup
from logs.logger import log
from logs.log_utils import log_json
import time, sys, random
from collections import namedtuple
from .utils import should_we_sleep, parse_user

BotAction = namedtuple("BotAction", 'name call')

class RedditBot():
  def __init__(self, config=reddit_config.CONFIG):
    self.api = reddit_api
    self.ready = False
    self.config = config
    self.user = None
    self.posts = Posts()
    self.comments = Comments()
    self.cleanup = Cleanup()
    self.actions = [
      BotAction('reddit_post_chance', self.posts.repost),
      BotAction('reddit_comment_chance', self.comments.comment),
      BotAction('reddit_shadowban_check', self.cleanup.shadow_check),
      BotAction('reddit_remove_low_scores', self.cleanup.remove_low_scores),
      BotAction('reddit_karma_limit_check', self.cleanup.karma_limit),
    ]

  def _init(self):
    # check if account is set
    user = self.api.user.me()
    if user is None:
      log.info("User auth failed, Reddit bot shutting down")
      sys.exit()
    else:
      log.info(f"running as user: {user}")
      
    # check if account is shadowbanned
    self.cleanup.init()
    self.cleanup.shadow_check()
    self.user = parse_user(user)
    log.info(f"account info:\n{log_json(self.user)}")
    self.ready = True
    log.info("The bot is now running. It has a chance to perform an action every second. Be patient")

  def tick(self):
    if not should_we_sleep():
      report = f""
      for action in self.actions:
        roll = random.random()
        result = roll < self.config[action.name] 
        print(f"{roll} < {self.config[action.name]} = {result}         ", end="\r")
        if result:
          log.info(f"\nrunning action: {action.name}")
          action.call()


  def run(self):
    if self.ready:
      self.tick()
    else:
      self._init()
      self.run()
      # log.info("not running reddit bot - not ready")
