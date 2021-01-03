from apis import pushshift_api, reddit_api
from utils import chance
import random
from .utils import get_subreddit, AVOID_WORDS
from config.reddit_config import CONFIG
from config.reddit.reddit_sub_lists import CROSSPOST_SUBS
from logs.logger import log
from praw.exceptions import APIException

class Posts():
  def __init__(self):
    self.psapi = pushshift_api
    self.rapi = reddit_api

  def get_post(self, subreddit=None):
    log.info(f"finding a post to re-post")    
    got_post = False
    attempts = 0
    while not got_post:
      # use the supplied subreddit
      # otherwise choose one randomy
      if subreddit:
        log.info(f"searching post in sub: {subreddit}")
        sub = self.rapi.subreddit(subreddit)
      else:
        # if there are subreddits in the subreddit list pull randomly from that
        # otherwise pull a totally random subreddit
        sub = self.rapi.subreddit(random.choice(CONFIG['reddit_sub_list'])) if CONFIG['reddit_sub_list'] else get_subreddit(getsubclass=True)
          
        log.info(f"searching post in sub: {sub.display_name}")
      try:
        post_id = self.psapi.get_posts(sub.display_name)[0]['id']
        # don't use posts have have avoid words in title
        if not any(word in comment.body for word in AVOID_WORDS):
          got_post = True
      except Exception as e:
        log.info(f"couldn't find post in {sub}")
        # sub = self.rapi.random_subreddit(nsfw=False)
        # log.info(f"trying in: {subreddit}")
        attempts += 1
        log.info(f"repost attempts: {attempts}")
        if attempts > 3:
          log.info(f"couldn't find any posts - skipping reposting for now")
          return

    return self.rapi.submission(id=post_id)

  def crosspost(self, subreddit):
    for idx, subs in enumerate(CROSSPOST_SUBS):
      if subs[0] == subreddit:
        return random.choice(subs[idx])


  def repost(self, roll=1, subreddit=None):
    if chance(roll):
      log.info("running repost")
      # log.info("running _repost")
      post = self.get_post(subreddit=subreddit)
      log.info(f"reposting post: {post.id}")

      if post.is_self:
        params = {"title": post.title, "selftext": post.selftext}
      else:
        params = {"title": post.title, "url": post.url}

      sub = post.subreddit

      # randomly choose a potential subreddit to cross post
      if CONFIG['reddit_crosspost_enabled']:
        sub = self.rapi.subreddit(self.crosspost(sub.display_name))

      try:
        self.rapi.subreddit(sub.display_name).submit(**params)
      except APIException as e:
        log.info(f"REPOST ERROR: {e}")
    else:
      pass
      # log.info("not running repost")
      # log.info("not running _repost")