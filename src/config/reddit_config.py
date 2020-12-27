from utils import prefer_envar
from logs.logger import log

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
  "reddit_post_chance": 0.05,
  # the chance the bot will make a comment
  "reddit_comment_chance": 0.5,
  # the chance the bot will reply to a comment
  # otherwise it will reply to a post
  "reddit_reply_to_comment": 0.35,
})

log.info(CONFIG)
