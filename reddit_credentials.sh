#!/bin/bash
# v 1.0
echo "# Reddit API" > .env

echo -e "Please enter your CLIENT_ID: "
read -r ID
echo "REDDIT_BOT_CLIENT_ID=\"$ID"\" >> .env

echo -e "Please enter your SECRET: "
read -r SE
echo "REDDIT_BOT_SECRET=\"$SE"\" >> .env

echo -e "Please enter your USERNAME: "
read -r UN
echo "REDDIT_BOT_USERNAME=\"$UN"\" >> .env

echo -e "Please enter your PASSWORD: "
read -r PW
echo "REDDIT_BOT_PASSWORD=\"$PW"\" >> .env

echo "done!"
