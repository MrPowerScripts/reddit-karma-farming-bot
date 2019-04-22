# Running This Bot on android

## Installation
Firstly Install termux from [This](https://play.google.com/store/apps/details?id=com.termux) Link and [Hacker's Keyboard](https://play.google.com/store/apps/details?id=org.pocketworkstation.pckeyboard) is also recomended for navigation in termux

Now open up termux and type in `pkg install git` 

After done type in `git clone https://github.com/EliteDaMyth/reddit-karma-farming-bot.git rkfb`

Now type in `cd rkfb` then `cd android`

Then to install the Deps run `bash install.sh`

Wait for it to finish and if it prompts anything agree to it

now type in `nano reddit.py`
Navigate to
```python
  api = praw.Reddit(client_id='REDDIT_CLIENT_ID',
                    client_secret='REDDIT_SECRET',
                    password=.'REDDIT_PASSWORD',
                    user_agent='REDDIT_USER_AGENT',
                    username='REDDIT_USERNAME')
```

and put in your Information to get client id and secret follow [This](https://hackernoon.com/build-a-serverless-reddit-bot-in-3-steps-with-node-js-and-stdlib-sourcecode-e5296b78fc64) Guide

now finally to run the bot use python2 run.py

HMU On Discord (EliteDaMyth#1592) for any questions/unexpected errors 

PEACE!
