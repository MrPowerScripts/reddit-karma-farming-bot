from .sources.cobe import Cobe
from logs.logger import log
from utils import chance
from apis import reddit_api
from config import reddit_config
from ..utils import get_subreddit
import random

class Comments():
  def __init__(self, source='cobe'):
    self.ready = False
    self.config = reddit_config.CONFIG
    self.rapi = reddit_api
    self.source = source
    self.cobe = Cobe()

  def init(self):
    log.info("intiializing comments")
    self.ready = False
    if self.source == "cobe":
      log.info("using cobe to generate comments")
      self.cobe.init()
    self.ready = True
    log.info("commenting ready")

  def comment(self, roll=1):
    if not self.ready:
      log.info("comments need to be initialized")
      self.init()

    if chance(roll):
      log.info("going to make a comment")
      
      # pick a subreddit to comment on
      subreddit = get_subreddit(getsubclass=True)
      # get a random hot post from the subreddit
      post = random.choice(list(subreddit.hot()))
      # replace the "MoreReplies" with all of the submission replies
      post.comments.replace_more(limit=0)
      # pick a comment, any comment

      if self.source == 'cobe':
        reply_getter = self.cobe.get_reply

      # choose if we're replying to the post or to a comment
      if chance(self.config.get('reddit_reply_to_comment')):
        # reply to the post with a response based on the post title
        log.info('replying directly to post')
        post.reply(reply_getter(post.title))
      else:
        # get a random comment from the post
        comment = random.choice(post.comments.list())
        # reply to the comment
        log.info('replying to comment')
        comment.reply(reply_getter(comment.body))

        



