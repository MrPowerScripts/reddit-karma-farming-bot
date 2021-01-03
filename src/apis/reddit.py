from praw import Reddit
from utils import random_string


class RedditAPI():
  def __init__(self,
              reddit_client_id,
              reddit_client_secret,
              reddit_password,
              reddit_username):

    self.client_id = reddit_client_id
    self.client_secret = reddit_client_secret
    self.password = reddit_password
    self.username = reddit_username
    self.user_agent = random_string(10)
    self.api = Reddit(
        client_id=self.client_id,
        client_secret=self.client_secret,
        password=self.password,
        user_agent=self.user_agent,
        username=self.username,
    )
