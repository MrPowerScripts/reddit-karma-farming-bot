#!/bin/bash
# v 1.0
echo "# Reddit API" >> src/settings.py

echo -e "Please enter your CLIENT_ID: "
read ID
echo "REDDIT_CLIENT_ID=\"$ID"\" >> src/settings.py

echo -e "Please enter your SECRET: "
read SE
echo "REDDIT_SECRET=\"$SE"\" >> src/settings.py

echo -e "Please enter your USERNAME: "
read UN
echo "REDDIT_USERNAME=\"$UN"\" >> src/settings.py

echo -e "Please enter your PASSWORD: "
read PW
echo "REDDIT_PASSWORD=\"$PW"\" >> src/settings.py

echo "REDDIT_USER_AGENT=\"This can be anything you want."\" >> src/settings.py
