from apis import pushshift_api, reddit_api
from actions import Action
from utils import chance
from logging import log

class Posts(Action):
  def __init__(self):
    self.psapi = pushshift_api
    self.rapi = reddit_api

  def repost(self, roll=None):
    roll = 1 if roll == None else roll
    if chance(roll):
      log.info("running repost")
      # log.info("running _repost")
      subreddit = self.api.random_subreddit(nsfw=False)
      log.info(f"reposting to {subreddit.display_name}")
      post = self.api.submission(id=self.psapi.get_posts(subreddit.display_name)[0]['id'])
      log.debug(post)

      if post.is_self:
        params = {"title": post.title, "selftext": post.selftext}
      else:
        params = {"title": post.title, "url": post.url}

      self.api.subreddit(subreddit.display_name).submit(**params)
    else:
      log.info("not running repost")
      # log.info("not running _repost")