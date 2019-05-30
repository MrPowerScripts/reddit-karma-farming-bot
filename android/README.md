# Running on android

## Installation

#### Install Termux

Install Termux from [here](https://play.google.com/store/apps/details?id=com.termux) and [Hacker's Keyboard](https://play.google.com/store/apps/details?id=org.pocketworkstation.pckeyboard) is also recommended for navigation in Termux.

#### Setup the bot

```python
# open up Termux app, type
pkg install git

# clone the repository
git clone https://github.com/MrPowerScripts/reddit-karma-farming-bot.git rkfb

# enter into the android directory of the bot
cd rkfb/android

# install requirements etc.
bash install.sh
```

The installation is done at this point, you just need to add reddit credentials.
type: `nano reddit.py`

Change the below lines, put your information into the appropriate places.
```python
  api = praw.Reddit(client_id='REDDIT_CLIENT_ID',
                    client_secret='REDDIT_SECRET',
                    password='REDDIT_PASSWORD',
                    user_agent='REDDIT_USER_AGENT',
                    username='REDDIT_USERNAME')
```

To get client id and secret follow [this](https://hackernoon.com/build-a-serverless-reddit-bot-in-3-steps-with-node-js-and-stdlib-sourcecode-e5296b78fc64) guide.

now finally to run the bot use `python2 run.py`

HMU On Discord (EliteDaMyth#1592) for any questions/unexpected errors or
join our dedicated Discord chat for more help @ https://bit.ly/mrps-discord  

PEACE!
