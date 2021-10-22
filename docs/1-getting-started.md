# Getting Started

## Creating the Reddit app

In your browser, when you are logged in with the Reddit account you want to use, go to this URL: https://www.reddit.com/prefs/apps

Once there, click the “are you a developer? create an app...” button at the bottom. Name the app anything you want, I recommend not naming it Reddit Karma bot. Instead, go for something generic like “Test script”. Then **CLICK THE SCRIPT OPTION**, this is important.

You can leave the description and about URL empty, but you need to put a value for the redirect URI. This can be anything as long as it is a valid URL. I recommend doing something similar to http://example.com or http://nourl.com. 

But like I said, it can be anything.

Then click Create App.
You will now be presented with this screen:

![app_example](https://user-images.githubusercontent.com/29954899/103455850-f8810880-4cf0-11eb-9002-64c2f1e5a44e.png)

In this image, you will find your client id and secret. The red highlight is your client id, and cyan is your secret key. Now we are ready to get the bot up and running!

## Using a proxy

The bot uses the Python `requests` library behind the scenes. Python `requests` library [has some enviroment variables you can set](https://stackoverflow.com/a/8287752) to have it automatically use a proxy server.

## Reddit Configuration

### How to configure the Reddit bot

The bot has many configuration options, and some are enabled/disabled by default. View all of the config options in the [src/config](/src/config) folder.

#### Limit to specific subreddits

Add subreddits to the `REDDIT_APPROVED_SUBS` variable [reddit_sub_lists.py](/src/config/reddit/reddit_sub_lists.py) file. This will limit the bot to only repost/learn/comment to these subreddits.

#### Avoid specific subreddits

Add the subreddits the bot should avoid to [reddit_avoid_subs.txt](/src/config/reddit/reddit_avoid_subs.txt) file, and the bot will ignore posting/commenting to these subreddits. Do not include `/r/`, just the clean subreddit name on each line of the file.

#### Avoid specific words

Add words the the bot should avoid to [reddit_avoid_words.txt](/src/config/reddit/reddit_avoid_words.txt) file, and the bot will ignore learning from comments, or reposting posts that include these words. Add a words on separate lines.

#### Configure what actions the Reddit bot performs

The reddit bot actions can be configured in [reddit_config.py](/src/config/reddit_config.py). If you don't want it to perform an action set the chance value to `0`. For instance, to disable commenting set `"reddit_comment_chance": 0.005,` to `"reddit_comment_chance": 0,`. Increasing the chance values will increase the chance the action is performed. The defualt values are fine, but you can experiment.

##### Sleep schedule

The bot has a sleep schedule enabled by default, otherwise it will comment/post 24/7 and likely get banned. You can disable the sleep schedule by removing all schedule values. Like `"reddit_sleep_schedule": [2, 4]` to `"reddit_sleep_schedule": []`.

#### Configure Cobe

Cobe is the library the bot uses to generate comments. You may want to conifgure how big the comment databse needs to be before it starts commeting. You can adjust the values in [cobe_config.py](/src/config/cobe_config.py).
