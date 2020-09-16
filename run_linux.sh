#!/usr/bin/env bash

DEBUG_FILE="./run_linux.log"
SETTINGS_FILE="./src/settings.py"

date '+%d/%m/%Y %H:%M:%S' | tee $DEBUG_FILE

if [[ $# -eq 0 ]] ; then
    echo "no arguments supplied - checking settings file" | tee -a $DEBUG_FILE
    if [[ ! -f "$SETTINGS_FILE" ]]; then
      echo "No ./src/settings.py file? You need to set the creds" | tee -a $DEBUG_FILE
      exit 1
    else
      echo "found settings file - gonna try that!" | tee -a $DEBUG_FILE
    fi
else
  echo "found arguments - I hope they're correct!" | tee -a $DEBUG_FILE
fi

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac
echo "system is ${machine}" | tee -a $DEBUG_FILE


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ ! -d "$DIR/venv" ]; then
  echo "no virtualenv detected doing setup before running" | tee -a $DEBUG_FILE
  echo "need to install dependencies" | tee -a $DEBUG_FILE
  if [ "${machine}" =  "Linux" ]; then
    echo "this is linux - install linux deps"
    apt-get update || { echo 'apt-get failed failed' | tee -a $DEBUG_FILE ; exit 1; }
    
    apt-get install -y --no-install-recommends \
      g++ \
      gcc \
      golang-go \
      libc6-dev \
      make \
      pkg-config \
      wget \
      tmux \
      python3.6 \
      python3-pip \
      python3-setuptools \
      python3-dev \
      git || { echo 'Installing dependencies failed' | tee -a $DEBUG_FILE ; exit 1; }
  elif [ "${machine}" =  "Mac" ]; then
    xcode-select --install
  else
    echo "No suitable linux version" | tee -a $DEBUG_FILE
  fi

  if [ "${machine}" =  "Linux" ] || [ "${machine}" =  "Mac" ]; then
    pip3 install virtualenv || { echo 'Installing virtualenv failed' | tee -a $DEBUG_FILE ; exit 1; }
    virtualenv -p "$(command -v python3)" venv || { echo 'Installing virtualenv failed' | tee -a $DEBUG_FILE ; exit 1; }
    source venv/bin/activate
    pip3 install cython
    pip3 install -r ./src/requirements.txt || { echo 'Installing python deps failed' | tee -a $DEBUG_FILE ; exit 1; }
  fi

fi



echo "activating the virtualenv " | tee -a $DEBUG_FILE
source venv/bin/activate

echo "trying to run the bot" | tee -a $DEBUG_FILE
python3 ./src/run.py "$@"

