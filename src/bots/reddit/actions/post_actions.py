from apis import pushshift_api, reddit_api
from actions import Action
from utils import chance
from logs.logger import log

class Posts(Action):
  def __init__(self):
    self.psapi = pushshift_api
    self.rapi = reddit_api

  def get_post(subreddit=None):
    if subreddit:
      # if no subreddit supplied choose randomly
      subreddit = self.rapi.subreddit(subreddit)
    else:
      subreddit = self.rapi.random_subreddit(nsfw=False)
    
    log.info(f"choosing subreddit: {subreddit}")
    
    return self.rapi.submission(id=self.psapi.get_posts(subreddit.display_name)[0]['id'])

  def repost(self, roll=1, subreddit=None):
    if chance(roll):
      log.info("running repost")
      # log.info("running _repost")
      post = self.get_post()
      log.debug(post)

      if post.is_self:
        params = {"title": post.title, "selftext": post.selftext}
      else:
        params = {"title": post.title, "url": post.url}

      self.rapi.subreddit(subreddit.display_name).submit(**params)
    else:
      log.info("not running repost")
      # log.info("not running _repost")