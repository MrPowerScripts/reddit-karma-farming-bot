# Getting Started

## Creating the Reddit app

In your browser, when you are logged in with the Reddit account you want to use, go to this URL: https://www.reddit.com/prefs/apps

Once there, click the “are you a developer? create an app...” button at the bottom. Name the app anything you want, I recommend not naming it Reddit Karma bot. Instead, go for something generic like “Test script”. Then **cCLICK THE SCRIPT OPTION**, this is important.

You can leave the description and about URL empty, but you need to put a value for the redirect URI. This can be anything as long as it is a valid URL. I recommend doing something similar to http://example.com or http://nourl.com. 

But like I said, it can be anything.

Then click Create App.
You will now be presented with this screen:

![app_example](https://user-images.githubusercontent.com/29954899/103455850-f8810880-4cf0-11eb-9002-64c2f1e5a44e.png)

In this image, you will find your client id and secret. These are highlighted in red and cyan respectively. Now we are ready to get the bot up and running!

## Configuration

### How to configure the bot

The bot has many configuration options, and some are enabled/disabled by default. View all of the config options in the [src/config](/src/config) folder.

### Environment Variables

Most settings can be cofigured through environment variables. The enviroment variable to configure a setting is the name of the setting prefixed by `BOT_` and fully uppercased. For example, the `reddit_client_id` config can be set with the envar `BOT_REDDIT_CLIENT_ID`.

The easiest way to configure the bot is by adding these enviroment variables to a `.env` file in the root of the repo, and the bot will automatically pick them up when run using `run_linux.sh`. The repo contains a sample `.env.sample` file you can rename to `.env`. Add the configuration envars you want and run the bot. You could also use a command like `env $(cat .env | xargs) && python3 ./src/init.py` to run the bot directly with all envars scoped locally. As well as any other method to apply envars which the bot will pick up and use when running.
