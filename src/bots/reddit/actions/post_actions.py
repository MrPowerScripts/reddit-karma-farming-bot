from apis import pushshift_api, reddit_api
from utils import chance
from .utils import get_subreddit
from logs.logger import log

class Posts():
  def __init__(self):
    self.psapi = pushshift_api
    self.rapi = reddit_api

  def get_post(self, subreddit=None):
    if subreddit:
      # if no subreddit supplied choose randomly
      subreddit = self.rapi.subreddit(subreddit)
    else:
      subreddit = get_subreddit(getsubclass=True)
    
    log.info(f"choosing subreddit: {subreddit}")
    
    got_post = False
    while not got_post:
      try:
        post_id = self.psapi.get_posts(subreddit.display_name)[0]['id']
        got_post = True
      except Exception as e:
        log.info(f"couldn't find post in {subreddit}")
        subreddit = self.rapi.random_subreddit(nsfw=False)
        log.info(f"trying in: {subreddit}")

    return self.rapi.submission(id=post_id)

  def repost(self, roll=1, subreddit=None):
    if chance(roll):
      log.info("running repost")
      # log.info("running _repost")
      post = self.get_post()
      log.info(f"reposting post: {post.id}")

      if post.is_self:
        params = {"title": post.title, "selftext": post.selftext}
      else:
        params = {"title": post.title, "url": post.url}

      self.rapi.subreddit(post.subreddit.display_name).submit(**params)
    else:
      pass
      # log.info("not running repost")
      # log.info("not running _repost")