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

## How to run the bot

1. Install docker https://docs.docker.com/install/
    - Make sure [you enable docker without sudo](https://docs.docker.com/install/linux/linux-postinstall/)

2. Update the environment variables below with your account info
    - Follow step 1 [of this guide](https://hackernoon.com/build-a-serverless-reddit-bot-in-3-steps-with-node-js-and-stdlib-sourcecode-e5296b78fc64) to get your app details such as client ID and secret


3. Paste the whole command below into your terminal

```bash
git clone https://github.com/MrPowerScripts/reddit-karma-farming-bot.git &&\
cd reddit-karma-farming-bot &&\
git pull origin master &&\
git reset --hard HEAD &&\
docker build -t=com.mrpowerscripts/mrps/reddit-karma-bot . &&\
mkdir -p ~/reddit-karma-bot/brain &&\
docker run -it \
  -e REDDIT_CLIENT_ID="MyCoolAppClientID" \
  -e REDDIT_SECRET="MyCoolAppSecret" \
  -e REDDIT_USERNAME="MyCoolUserName" \
  -e REDDIT_PASSWORD="MyPasswordForTheUsername" \
  -e REDDIT_USER_AGENT="script by /u/" \
  -p 8080:8080 \
  --mount src=~/reddit-karma-bot,target=/reddit-karma-bot,type=bind \
  com.mrpowerscripts/mrps/reddit-karma-bot
```

### Windows

The command above will not readily work on Docker for Windows. Try running each command individually (lines between the `&&`) and put each command on a single line (remove the `\` from each command). If you get a fully working oneliner on Windows do let me know!

You can provide a proxy server for the docker container to connect through

```bash
--e HTTPS_PROXY="https://127.0.0.1:3001"
```

## The deets

- When the docker container is running you can start the bot by browsing to https://127.0.0.1:8080 The default username pass is admin/pass. It will give you an SSL warning because the CA is self-signed. Just click whatever button allowys you to pass through the warning.
- The bot will store all of the stuff in learns in a folder within your home path (~) called `reddit-karma-bot`.
- The bot will wait until it has 50MB worth of material learned before it will start commenting. This can take a while. The logs on the browser will tell you everything that is happening. There will also be a info.log in the `reddit-karma-bot` folder.