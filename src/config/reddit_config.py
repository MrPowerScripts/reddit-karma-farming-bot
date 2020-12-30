from utils import prefer_envar
from logs.logger import log
import sys
import json
import os

if os.path.isfile('config.json'):
  file = open("config.json", "r")
  AUTH = prefer_envar(json.loads(file.read()))
else:
  AUTH = prefer_envar({
    # app creds
    "reddit_client_id":"",
    "reddit_client_secret":"",
    # reddit account creds
    "reddit_username":"",
    "reddit_password":"",
  })

log.info(AUTH)

CONFIG = prefer_envar({
  # the chance the bot will repost a post
  "reddit_post_chance": 0.005,
  # the chance the bot will make a comment
  "reddit_comment_chance": 0.005,
  # the chance the bot will reply to a comment
  # otherwise it will reply to a post
  "reddit_reply_to_comment": 0.002,
  # chance the bot will remove poor performing
  # posts and comments
  "reddit_remove_low_scores": 0.002,
  # posts/comments that get downvoted to this score will be deleted
  "reddit_low_score_threshold": 0,
  # chance to check if the bot is shadowbanned, 
  # and shut down the script automatically
  "reddit_shadowban_check": 0.002,
})

log.info(CONFIG)
