# Reddit-Karma-Bot

This bot is probably the reason you saw that post again on Reddit. Need help with the bot? Join us on Discord https://bit.ly/mrps-discord 

![farm karma 1](https://user-images.githubusercontent.com/1307942/86540032-7e1a2c00-bef9-11ea-9266-16830c5b9dfa.png)
![farm karma bot](https://user-images.githubusercontent.com/1307942/86153469-a40a8f80-baf9-11ea-80b5-d86dd31108d6.png)

### 2020 update videos
[Definitely Watch This One](https://www.youtube.com/watch?v=nWYRGXesb3I)

[2020 Bot 3.0 Code Walkthrough](https://www.youtube.com/watch?v=83zWIz3b7o0)

### Older videos

[Karma Farming Bot 2.0 Video](https://www.youtube.com/watch?v=CCMGHepPBso)  
[Karma Farming on Reddit Video](https://www.youtube.com/watch?v=8DrOERA5FGc)  
[Karma Farming Bot 1.0 Video](https://www.youtube.com/watch?v=KgWsqKkDEtI)  

Subscribe: http://bit.ly/mrps-yt-sub  
Website: https://bit.ly/mrps-site  

## Features

- Run on Linux, MacOS, or Windows (using Linux in VirtualBox).
- Automatically reposts popular posts from the past to earn post karma.
- Automatically generates unique (somewhat) contextually relevant comments using [cobe](https://github.com/pteichman/cobe).
- Automatically deletes poor performing comments and posts.
- Configurable frequency of posting, commenting, and other actions.
- Filter the bot from learning certain words, or avoid certain subreddits.
- Schedule when the bot wakes up and sleeps to run actions.
- Auto detects if the account is shadowbanned.

## Getting Started

1. Follow the [getting started guide](docs/1-getting-started.md) to create your Reddit app.

2. Then follow the [macOS/Linux](docs/2-liunx-macos.md), or [Windows](docs/3-windows.md) guides.

## Configuration

### How to configure the bot

The bot has many configuration options, and some are enabled/disabled by default. View all of the config options in the [src/config](src/config) folder.

### Environment Variables

All of the bot settings can be cofigured through environment variables. The enviroment variable to configure a setting is the name of the setting prefixed by `BOT_` and fully uppercased. For example, the `reddit_client_id` config can be set with the envar `BOT_REDDIT_CLIENT_ID`. You can add these enviroment variables to a `.env` file in the root of the repo, and the bot will automatically pick them up when run using `run_linux.sh`.

## How to run the bot on Linux/MacOS

1. Change `.env.sample.py` to `.env` and update the values to your account and app values.

2. run `run_linux.sh`

## Warnings

### Reddit

New Reddit accounts will likely get banned with the bot. Let an account sit for a few days before using it. Do not use an account that you love, as it's possible to be permanently banned.

### Heroku

The bot used to have a Heroku option - till they found out and now using the bot on heroku will get your account banned.