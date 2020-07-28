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
- Run on Linux, MacOS, Docker, or Windows (WSL2, or Ubuntu in [VirtualBox](https://www.virtualbox.org/))
- Charts that show Brain database size, and Post/Comment Karma growth over time
- Uses proxies with [requests library](https://2.python-requests.org/en/master/user/advanced/#id10) envars like: `HTTPS_PROXY="https://127.0.0.1:3001` 

![Karma Charts](https://user-images.githubusercontent.com/1307942/86981035-67840700-c17d-11ea-9e6b-828e1ad2dd9c.png)

## Configuration

Most of these options can be configured in [utils.py](src/utils.py)

## Prep 🔈(!!YOU MUST DO THIS FIRST!!)🔈

First, you need to create a Reddit account, and then create an app on reddit.com. After creating a Reddit account [go here to create an app](https://old.reddit.com/prefs/apps/). follow step 1 [of this guide](https://hackernoon.com/build-a-serverless-reddit-bot-in-3-steps-with-node-js-and-stdlib-sourcecode-e5296b78fc64) to learn how to create the app and get your app details such as client ID and secret


## Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/psywarrior1998/reddit-karma-farming-bot)

**Important Note: If you restart the Heroku Dyno it will reset the database. Heroku is good if you have absolutely no coding experience at all and just want to see it in action. Otherwise, you're better off installing and running the bot on Ubuntu**

After deploying it and it says deployed click on `Manage App` Button

Now click `Resources` tab

Click on the `Edit` Icon and turn on the worker and save

Click on `more` and `view logs` to make sure everything is fine

That's it, Your Free Hosting is complete!

## Windows 10 (WSL2)

Please look here for a detailed guide to running on windows 10 / Linux. The other guides in this readme also work, but this is more step-by-step.
[Click here for the google docs link](https://docs.google.com/document/d/1we5QR5E1nVNz862OG40oic9lnYhULStkWKlprmYlKFo/edit?usp=sharing)

## Linux/MacOS
Designed for Ubuntu 20. MacOS may require manually installing some deps through brew.


1. change `src/settings.sample.py` to `src/settings.py` and update the values to your account and app values

1. run `run_linux.sh`

