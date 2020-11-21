# Reddit-Karma-Bot

This bot is probably the reason you saw that post again on Reddit. Need help with the bot? Join us on Discord https://bit.ly/mrps-discord 

![farm karma 1](https://user-images.githubusercontent.com/1307942/86540032-7e1a2c00-bef9-11ea-9266-16830c5b9dfa.png)
![farm karma bot](https://user-images.githubusercontent.com/1307942/86153469-a40a8f80-baf9-11ea-80b5-d86dd31108d6.png)

### 2020 update videos
[Definitely Watch This One](https://www.youtube.com/watch?v=nWYRGXesb3I)

[2020 Bot Code Walkthrough](https://www.youtube.com/watch?v=83zWIz3b7o0)

### Older videos

[Karma Farming Bot 2.0 Video](https://www.youtube.com/watch?v=CCMGHepPBso)  
[Karma Farming on Reddit Video](https://www.youtube.com/watch?v=8DrOERA5FGc)  
[Karma Farming Bot 1.0 Video](https://www.youtube.com/watch?v=KgWsqKkDEtI)  

Subscribe: http://bit.ly/mrps-yt-sub  
Website: https://bit.ly/mrps-site  

## Features

- Automatically reposts popular posts from the past to earn post karma
- Automatically generates unique (somewhat) contextually relevant comments using [cobe](https://github.com/pteichman/cobe)
- Automatically deletes poor performing comments
- Configurable frequency of posting, commenting, and other actions
- Filter the bot from learning certain words, or allow/disallow certain subreddits
- Schedule when the bot wakes up and sleeps to run actions.
- Auto detects if the account is shadowbanned
- Use Spinwriter API to mix up comments and titles, making them less detectable as reposts
- Re-upload images to Imgur to make reposts less detectable
- Limit the subreddits that the bot learns from and posts to
- Run on Linux, MacOS, Docker, or Windows (using Linux in VirtualBox)
- Charts that show Brain database size, and Post/Comment Karma growth over time

![Karma Charts](https://user-images.githubusercontent.com/1307942/86981035-67840700-c17d-11ea-9e6b-828e1ad2dd9c.png)

## Warnings
The bot used to have a Heroku option - till they found out and now using the bot on heroku will get your account banned. 
New accounts will likely get banned with the bot. Let an account sit for a few days before using it. Do not use an account that you don't want to lose.

## Configuration

Most of these options can be configured in [utils.py](src/utils.py)

### Configuration notes

The bot has many configuration options, and some are enabled/disabled by default.

#### Commments

By default, the bot will not generate comments. You can turn on bot commenting by setting `COMMENTS_DISABLED` to `False`. If you turn on commenting the bot will need around eight hours to learn before it will perform any actions. Once it has learned enough data to meet the `MAIN_DB_MIN_SIZE` it will start performing all actions. The bot will continue to learn sometimes aftre reaching `MAIN_DB_MIN_SIZE`, but will stop once it reaches `MAIN_DB_MAX_SIZE`. If comments are disabled the bot will start performing all other actions imediately. The bot ignores default nsfw subreddits by default.

#### Subreddits

You can limit the bot to specific subreddits for posting and commenting by adding them to `SUBREDDIT_LIST`. This is SIGNIFICANTLY slow down the bot learning if you have commenting enabled. Especially if are only adding smaller subreddits. If your db size is growing very slowly this is likely why. Add more bigger subreddits, or leave the list empty and the bot will select subreddits randomly.

#### Bot Actions

The bot runs on a one second loop, and each loop there's a chance it will perform an action. One of the following actions:

1. `shadowcheck`: Check to see if the account is shadowbanned. If it's shadowbanned the bot will automatically stop.
1. `karmacheck`: Check how much comment/post karma the account currently has, and save it in tinydb `db.json`
1. `dbcheck`: Check the size of the sqlite `brain.db`, and save it in tinydb `db.json`
1. `reply`: Reply to a post/comment on a random post
1. `submit`: Re-post a random post from around `NUMBER_DAYS_FOR_POST_TO_BE_OLD` days ago with at least `SUBREDDIT_THRESHOLD` upvotes on the post.
1. `delete`: Automatically delete posts and comments the bot made that have a score lower than `SCORE_THRESHOLD`.

You can increase the chance of each action triggering by increasing the probability for the action:

```python
PROBABILITIES = {
  "REPLY": 0.002,
  "SUBMISSION": 0.005,
  "SHADOWCHECK": 0.002,
  "DBCHECK": 0.005,
  "KARMACHECK" : 0.005,
  "LEARN": 0.02,
  "DELETE": 0.02 }
```

Higher numbers will increse the chance. The defaults are fine, don't get too greedy or you'll hit API limits.

#### Sleep Schedule

By default the bot has `USE_SLEEP_SCHEDULE` set to `True`. This means that the bot will spend most of its time sleeping, and only post for a few hours per day to simulate a regular persons schedule. You can disable this, but then the bot will likely post too often and get caught/banned.

You can edit the bots sleep schedule. It can have multiple sleep/awake cycles per day. The `days` value is the number of days since the bot was first started to start using that schedule. This allows you to have the bot automatically adjust which schedule to use over time.

```python
BOT_SCHEDULES = [
  {"days": 0, "schedule": [((4,00),(5,00)), ((17,30),(19,30))]},
  {"days": 4, "schedule": [((8,00),(10,00)), ((20,30),(23,20))]},
  ]
```

The sleep schedule output will look like this:
`2020-08-31T20:13:03.823059+00:00 app[worker.1]: 2020-08-31 20:13:03,822 INFO should_we_sleep(97) using schedule: {'days': 0, 'schedule': [(datetime.time(4, 0), datetime.time(5, 0)), (datetime.time(17, 30), datetime.time(19, 30))]}`

We can see it says which schedule its using. Let's break the schedule into smaller chunks to see how to read it. This is the schedule configuration value, you'll notice it's an array:
`[(datetime.time(4, 0), datetime.time(5, 0)), (datetime.time(17, 30), datetime.time(19, 30))]`

The  array is made of datetime tuples. The first element of the tuple should be an awake time, and the second will be the sleep time.

`(datetime.time(4, 0), datetime.time(5, 0))`

Each item in the tuple is just a 24 hour clock value. So `5:30pm` would be `datetime.time(17,30)`

`datetime.time(4, 0)`

## Prep (!!YOU MUST DO THIS FIRST!!)

First, you need to create a Reddit account, and then create an app on reddit.com. After creating a Reddit account [go here to create an app](https://old.reddit.com/prefs/apps/). follow step 1 [of this guide](https://hackernoon.com/build-a-serverless-reddit-bot-in-3-steps-with-node-js-and-stdlib-sourcecode-e5296b78fc64) to learn how to create the app and get your app details such as client ID and secret

## In Depth guide to running on Windows / Linux

**WSL is currently not supported. Please install Ubuntu in Virtualbox and use Linux instructions if you want to run it on Windows**
Please look here for a detailed guide to running on windows 10 / Linux. The other guides in this readme also work, but this is more step-by-step.
[Click here for the google docs link](https://docs.google.com/document/d/1we5QR5E1nVNz862OG40oic9lnYhULStkWKlprmYlKFo/edit?usp=sharing)

## How to run the bot on Linux/MacOS

1.a. run `sudo sh reddit_credentials.sh` . 
**OR**
1.b. change `src/settings.sample.py` to `src/settings.py` and update the values to your account and app values.

1. run `run_linux.sh`.

## How to run the bot with docker

1. Install docker https://docs.docker.com/install/
    - Make sure [you enable docker without sudo](https://docs.docker.com/install/linux/linux-postinstall/)

2. Update the environment variables below with your account info

3. Paste the whole command below into your terminal

```bash
git clone https://github.com/MrPowerScripts/reddit-karma-farming-bot.git &&\
cd reddit-karma-farming-bot &&\
docker build -t=com.mrpowerscripts/mrps/reddit-karma-bot . &&\
docker run -it \
  -e REDDIT_CLIENT_ID="MyCoolAppClientID" \
  -e REDDIT_SECRET="MyCoolAppSecret" \
  -e REDDIT_USERNAME="MyCoolUserName" \
  -e REDDIT_PASSWORD="MyPasswordForTheUsername" \
  -e REDDIT_USER_AGENT="script by /u/" \
  --mount src="$(pwd)/src",target=/reddit-karma-bot-run,type=bind \
  com.mrpowerscripts/mrps/reddit-karma-bot
```

- The bot will store all of the stuff it learns in a folder within your home path (~) called `reddit-karma-bot`.
- The bot will wait until it has 50MB worth of material learned before it will start commenting. This can take a while. The logs on the browser will tell you everything that is happening. There will also be a info.log in the `reddit-karma-bot` folder.

You can provide also a proxy server for the docker container to connect through

```bash
--e HTTPS_PROXY="https://127.0.0.1:3001"
```
