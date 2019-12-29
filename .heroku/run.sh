#!/usr/bin/env bash

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac
echo "${machine}"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ ! -d "$DIR/venv" ]; then
  echo "need to install dependencies"
  if [ "${machine}" =  "Linux" ]; then
    echo "this is linux - install linux deps"
    sudo apt-get update && \
      sudo apt-get install -y --no-install-recommends \
        g++ \
        gcc \
        golang-go \
        libc6-dev \
        make \
        pkg-config \
        wget \
        tmux \
        python2.7 \
        python-pip \
        python-setuptools \
        python-dev \
        git 

    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip2 install wheel
    pip2 install --upgrade pip wheel -r ../src/requirements.txt

  else
    echo "No suitable linux version"
  fi
fi

source venv/bin/activate
python2.7 ../src/run.py
