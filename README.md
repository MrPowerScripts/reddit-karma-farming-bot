# Reddit talkbot

[Video: Is reddit full of robots?](https://www.youtube.com/watch?v=8DrOERA5FGc)


[Video: Reddit Chat Bot](https://www.youtube.com/watch?v=KgWsqKkDEtI)

## Install OS dependencies (I'm running Ubuntu 16)
> sudo apt-get install git python-pip python-dev build-essential 

> sudo pip install virtualenv

## Clone the repo, and open the directory
> git clone https://github.com/MrPowerScripts/talkbot.git

> cd talkbot

## Create a python virtual environment
> virtualenv venv

## Activate the python virtual environment
> source venv/bin/activate

## Install dependencies
> pip install -r requirements.txt

## Update settings.py with your Reddit bot account info
You can get the settings info by logging into reddit and going to https://www.reddit.com/prefs/apps/

Create an app, and use the app info in settings.py

## Run learn.py to have the bot start learning from reddit
> python learn.py

## Run talk.py to have the bot start replying/posting on reddit.
> python talk.py
