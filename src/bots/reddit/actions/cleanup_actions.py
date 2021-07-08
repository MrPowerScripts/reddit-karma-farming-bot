import praw
import requests
from apis import pushshift_api, reddit_api
from config import reddit_config
from utils import chance
from logs.logger import log
import sys

class Cleanup():
  def __init__(self):
    self.psapi = pushshift_api
    self.rapi = reddit_api
    self.username = None

  def init(self):
    self.me = self.rapi.user.me
    self.username = self.me().name

  def shadow_check(self, roll=1):
    if chance(roll):
      log.info("performing a shadowban check")
      response = requests.get(f"https://www.reddit.com/user/{self.username}/about.json",  headers = {'User-agent': f"hiiii its {self.username}"}).json()
      if "error" in response:
        if response["error"] == 404:
          log.info(f"account {self.username} is shadowbanned. poor bot :( shutting down the script...")
          sys.exit()
        else:
          log.info(response)
      else:
        log.info(f"{self.username} is not shadowbanned! We think..")

  def remove_low_scores(self, roll=1):
    comment_count = 0
    post_count = 0
    if chance(roll):
      log.info("checking for low score content to remove")
      for i in self.rapi.redditor(self.username).new(limit=500):
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

  def karma_limit(self):
    # current karma limit
    ckl = reddit_config.CONFIG["reddit_comment_karma_limit"]
    # current post karma
    cck = self.me().comment_karma
    # post karma limit
    pkl = reddit_config.CONFIG["reddit_post_karma_limit"]
    # current post karma
    cpk = self.me().link_karma

    if ckl:
      if ckl < cck:
        log.info(f"Comment karma limit ({ckl}) exceeded! Your current comment karma: {cck}. Shutting down the script.")
        sys.exit()
      else:
        log.info(f"Comment karma limit ({ckl}) not reached. Current comment karma: {cck}")
        return
    
    if pkl:
      if pkl < cpk:
        log.info(f"Post karma limit ({pkl}) exceeded! Your current post karma: {cpk}. Shutting down the script.")
        sys.exit()
      else:
        log.info(f"Post karma limit ({pkl}) not reached. Current post karma: {cpk}")
        return

    log.info(f"No limits - ignoring.")

