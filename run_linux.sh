#!/usr/bin/env bash

DEBUG_FILE="./run_linux.log"
export PIPENV_VENV_IN_PROJECT=1

date '+%d/%m/%Y %H:%M:%S' | tee $DEBUG_FILE

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

if [ ! -d "$DIR/.venv" ]; then
  echo "no virtualenv detected doing setup before running" | tee -a $DEBUG_FILE
  echo "need to install dependencies" | tee -a $DEBUG_FILE
  if [ "${machine}" =  "Linux" ]; then
    echo "this is linux - install linux deps"
    apt-get update || { echo 'apt-get failed failed' | tee -a $DEBUG_FILE ; exit 1; }

    apt-get install -y --no-install-recommends \
      g++ \
      gcc \
      libc6-dev \
      make \
      pkg-config \
      libffi-dev \
      python3.6 \
      python3-pip \
      python3-setuptools \
      python3-dev \
      git || { echo 'Installing dependencies failed' | tee -a $DEBUG_FILE ; exit 1; }
  elif [ "${machine}" =  "Mac" ]; then
    $(xcode-select -p) || xcode-select --install
  else
    echo "No suitable linux version!" | tee -a $DEBUG_FILE
  fi

  if [ "${machine}" =  "Linux" ] || [ "${machine}" =  "Mac" ]; then
    pip3 install pipenv || { echo 'Installing virtualenv failed' | tee -a $DEBUG_FILE ; exit 1; }
    pipenv install || { echo 'Installing python dependencies failed' | tee -a $DEBUG_FILE ; exit 1; }
  fi
fi

echo "Trying to run the bot" | tee -a $DEBUG_FILE

# start bot directly if nomenu passed in to script
if [[ $1 == *"menu"* ]]; then
  echo "Running with menu" | tee -a $DEBUG_FILE
  pipenv run python3 ./src/menu.py "$@"
else
  echo "Running without menu" | tee -a $DEBUG_FILE
  pipenv run python3 ./src/init.py "$@"
fi
