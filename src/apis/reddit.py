from praw import Reddit
from utils import random_string


class RedditAPI():
  def __init__(self,
              client_id,
              client_secret,
              password,
              username):

    self.client_id = client_id
    self.client_secret = client_secret
    self.password = password
    self.username = username
    self.user_agent = random_string(10)
    self.api = Reddit(
        client_id=self.client_id,
        client_secret=self.client_secret,
        password=self.password,
        user_agent=self.user_agent,
        username=self.username,
    )
