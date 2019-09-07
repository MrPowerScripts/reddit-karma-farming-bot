# Reddit-Karma-Bot

## Shameless self promotion

[Karma Farming Bot 2.0 Video](https://www.youtube.com/watch?v=CCMGHepPBso)  
[Karma Farming on Reddit Video](https://www.youtube.com/watch?v=8DrOERA5FGc)  
[Karma Farming Bot 1.0 Video](https://www.youtube.com/watch?v=KgWsqKkDEtI)  

Subscribe: http://bit.ly/mrps-yt-sub  
Website: https://bit.ly/mrps-site  
Discord: https://bit.ly/mrps-discord  
Patreon: https://bit.ly/mrps-patreon  
Power Up!: https://bit.ly/mrps-powerup  

## Prep

First you need to create a reddit account, and then create an app on reddit.com. After creating a reddit account follow step 1 [of this guide](https://hackernoon.com/build-a-serverless-reddit-bot-in-3-steps-with-node-js-and-stdlib-sourcecode-e5296b78fc64) to get your app details such as client ID and secret

## For Android running visit the android folder

## How to run the bot on Linux

1. change `src/settings.sample.py` to `src/settings.py` and update the values to your acccount and app values

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

- When the docker container is running you can start the bot by browsing to https://127.0.0.1:8080 The default username pass is admin/pass. It will give you an SSL warning because the CA is self-signed. Just click whatever button allowys you to pass through the warning.
- The bot will store all of the stuff in learns in a folder within your home path (~) called `reddit-karma-bot`.
- The bot will wait until it has 50MB worth of material learned before it will start commenting. This can take a while. The logs on the browser will tell you everything that is happening. There will also be a info.log in the `reddit-karma-bot` folder.

You can provide also a proxy server for the docker container to connect through

```bash
--e HTTPS_PROXY="https://127.0.0.1:3001"
```

### Windows

The command above will not readily work on Docker for Windows. Try running each command individually (lines between the `&&`) and put each command on a single line (remove the `\` from each command). If you get a fully working oneliner on Windows do let me know!
