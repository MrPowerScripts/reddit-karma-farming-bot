import praw
from apis import pushshift_api, reddit_api
from config import reddit_config
from utils import chance
from logs.logger import log

class Cleanup():
  def __init__(self):
    self.psapi = pushshift_api
    self.rapi = reddit_api

  def remove_low_scores(self, roll=1):
    comment_count = 0
    post_count = 0
    if chance(roll):
      log.info("checking for low score content to remove")
      for i in self.rapi.redditor(self.rapi.user.me().name).new(limit=500):
        if i.score <= reddit_config.CONFIG["reddit_low_score_threshold"]:
          if isinstance(i, praw.models.Comment):
            log.info(f"deleting comment(id={i.id}, body={i.body}, score={i.score}, subreddit={i.subreddit_name_prefixed}|{i.subreddit_id})")
            try:
              i.delete()
            except Exception as e:
              log.info(f"unable to delete comment(id={i.id}), skip...\n{e.message}")
            comment_count += 1
          else:
            log.info(f"deleting post(id={i.id}, score={i.score}, subreddit={i.subreddit_name_prefixed}|{i.subreddit_id})")
            try:
              i.delete()
            except Exception as e:
              log.info(f"unable to delete post(id={i.id}), skip...\n{e.message}")
            post_count += 1
            
          log.info(f'removed {comment_count + post_count} item(s). removed {comment_count} comment(s), {post_count} post(s) with less than {reddit_config.CONFIG["reddit_low_score_threshold"]} score')
      
      # GOOD BOT
      if (comment_count + post_count) == 0:
        log.info("no low score content to clean up. I'm a good bot! :^)")
