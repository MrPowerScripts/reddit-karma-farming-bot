import configparser
import praw
import os
import sys
from prawcore import ResponseException
from ..common_config import ENV_FILE

# create configparser object
config_file = configparser.ConfigParser()
config_file.optionxform = str


def config_gen():
    if not os.path.isfile(ENV_FILE):
      # ASK FOR CREDENTIALS
    def CI():
        CLIENT_ID = input('please input your account client id :')
        if len(CLIENT_ID) == 14 :
            pass
        else:
            log.info("client id must be 14 characters, try again")
            CI()
    CI()
    def SI():
        CLIENT_SECRET = input('please input your account client secret :')
        if len(CLIENT_SECRET) == 30 :
            pass
        else:
            log.info("client secret must be 30 characters, try again")
            SI()
    SI()
    PASSWORD = input('please input your account password :')
    def UN():
        USERNAME = input('please input your account username :')
        if len(USERNAME) in range(21) :
            pass
        else:
            UN()
    UN()


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

      config_file["DOTENV"] = {
          "BOT_REDDIT_CLIENT_ID": '"' + CLIENT_ID + '"',
          "BOT_REDDIT_CLIENT_SECRET": '"' + CLIENT_SECRET + '"',
          "BOT_REDDIT_PASSWORD": '"' + PASSWORD + '"',
          "BOT_REDDIT_USERNAME": '"' + USERNAME + '"',
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

