#!/bin/bash
set -ex
mkdir brains
apt install nano
apt install git
apt install python2
apt install python-dev
apt install python-setuptools
apt install sqlite
apt install libsqllite-dev
apt install libffi-dev
python2 install -r requirements.txt
echo "Everything Now Installed Please setup your credentials in reddit.py using nano reddit.py then run the bot using python2 run.py"
