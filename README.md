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
- Limit the subreddits that the bot learns from and posts to
- Run on Linux, MacOS, Docker, or Windows (using Linux in VirtualBox)
- Charts that show Brain database size, and Post/Comment Karma growth over time

![Karma Charts](https://user-images.githubusercontent.com/1307942/86981035-67840700-c17d-11ea-9e6b-828e1ad2dd9c.png)

## Configuration

Most of these options can be configured in [utils.py](src/utils.py)

## Prep (IMPORTANT)

First, you need to create a Reddit account, and then create an app on reddit.com. After creating a Reddit account [go here to create an app](https://old.reddit.com/prefs/apps/). follow step 1 [of this guide](https://hackernoon.com/build-a-serverless-reddit-bot-in-3-steps-with-node-js-and-stdlib-sourcecode-e5296b78fc64) to learn how to create the app and get your app details such as client ID and secret

## NEW! Run it on Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/MrPowerScripts/reddit-karma-farming-bot)

**Important Note: If you restart the Heroku Dyno it will reset the database. We don't have a way of externalizing it at the moment. You cannot easily make modifications to the code because it pulls directly from this repo, and therefore you cannot easily change any config options. Heroku is good if you have absolutely no coding experience at all and just want to see it in action. Otherwise, you're better off installing and running the bot on Ubuntu**

After deploying it and it says deployed click on `Manage App` Button

Now click `Resources` tab

Click on the Edit Icon and turn on the worker and save

Click on more and view logs to make sure everything is fine

Thats it, Your Free Hosting is complete!

## In Depth guide to running on Windows / Linux

**WSL is currently not supported. Please either use heroku or install Ubuntu in Virtualbox and use Liux instructions**
Please look here for a detailed guide to running on windows 10 / Linux. The other guides in this readme also work, but this is more step-by-step.
[Click here for the google docs link](https://docs.google.com/document/d/1we5QR5E1nVNz862OG40oic9lnYhULStkWKlprmYlKFo/edit?usp=sharing)

## How to run the bot on Linux/MacOS

1. change `src/settings.sample.py` to `src/settings.py` and update the values to your account and app values

1. run `run_linux.sh`

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

- When the docker container is running you can start the bot by browsing to https://127.0.0.1:8080 The default username pass is admin/pass. It will give you an SSL warning because the CA is self-signed. Just click whatever button allows you to pass through the warning.
- The bot will store all of the stuff it learns in a folder within your home path (~) called `reddit-karma-bot`.
- The bot will wait until it has 50MB worth of material learned before it will start commenting. This can take a while. The logs on the browser will tell you everything that is happening. There will also be a info.log in the `reddit-karma-bot` folder.

You can provide also a proxy server for the docker container to connect through

```bash
--e HTTPS_PROXY="https://127.0.0.1:3001"
```
