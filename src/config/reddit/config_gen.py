import configparser
import praw
import sys
import os
from logs.logger import log
from prawcore import ResponseException
from ..common_config import ENV_FILE

# create configparser object
config_file = configparser.ConfigParser()
config_file.optionxform = str


def config_gen():
  # ASK FOR CREDENTIALS
  CLIENT_ID = input('please input your account client id :')
  CLIENT_SECRET = input('please input your account client secret :')
  PASSWORD = input('please input your account password :')
  USERNAME = input('please input your account username :')

  reddit = praw.Reddit(
      client_id=CLIENT_ID,
      client_secret=CLIENT_SECRET,
      user_agent="my user agent",
      username=USERNAME,
      password=PASSWORD
  )
  # CHECK IF CREDENTIALS ARE CORRECT

  def authenticated(reddit):
      try:
          reddit.user.me()
      except ResponseException:
          return False
      else:
          return True

  config_file["REDDIT_AUTH"] = {
      "bot_reddit_client_id": f'"{CLIENT_ID}"',
      "bot_reddit_client_secret": f'"{CLIENT_SECRET}"',
      "bot_reddit_password": f'"{PASSWORD}"',
      "bot_reddit_username": f'"{USERNAME}"',
  }

  # SAVE CONFIG FILE
  if authenticated(reddit) is True:
      with open(ENV_FILE, "w") as file_object:
          config_file.write(file_object, space_around_delimiters=False)
          print("Config file '.env' created. Please re-run the bot")
          sys.exit()
          
  else:
      print('  WRONG CREDENTIALS ! ')
      print(' PLEASE INPUT CORRECT CREDENTIALS .')
      config_gen()

