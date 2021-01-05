import configparser
import praw
from prawcore import ResponseException

# create configparser object
config_file = configparser.ConfigParser()

while True:
    
    CLIENT_ID=input('please your account input id :')
    CLIENT_SECRET=input('please your account input secret :')
    PASSWORD=input('please input your account password :')
    USERNAME=input('please input your account username :')

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent="my user agent",
        username=USERNAME,
        password=PASSWORD
    )

    def authenticated(reddit):
        try:
            reddit.user.me()
        except ResponseException:
            return False
        else:
            return True

    config_file["DOTENV"] = {
        "BOT_REDDIT_CLIENT_ID":'"'+ CLIENT_ID +'"',
        "BOT_REDDIT_CLIENT_SECRET":'"'+ CLIENT_SECRET +'"',
        "BOT_REDDIT_PASSWORD":'"'+ PASSWORD +'"',
        "BOT_REDDIT_USERNAME":'"'+  USERNAME +'"',
    }

    # SAVE CONFIG FILE
    if authenticated(reddit) is True:
        with open(".env", "w") as file_object:
            config_file.write(file_object,space_around_delimiters=False)
            print("Config file '.env' created")
        break
    else:
        print('  WRONG CREDENTIALS ! ')
        print(' PLEASE INPUT CORRECT CREDENTIALS .')
