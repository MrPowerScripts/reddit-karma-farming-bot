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

if [ "$1" = "setup" ]; then
  if [ "${machine}" =  "Linux" ]; then
    apt-get update && \
      apt-get install -y --no-install-recommends \
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
  else
    echo "nada"
  fi

  pip install virtualenv
  virtualenv venv
  source venv/bin/activate
  pip2 install wheel
  pip2 install --upgrade pip wheel -r ./src/requirements.txt

else
  source venv/bin/activate
  python2.7 ./src/run.py
fi
