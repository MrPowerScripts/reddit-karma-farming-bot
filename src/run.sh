#!/bin/bash
set -ex

mkdir -p /reddit-karma-bot-run
cp -rf /reddit-karma-bot-src/* /reddit-karma-bot-run || true
mkdir -p /reddit-kamra-bot-run/brains || true
mkdir -p /reddit-karma-bot/brains || true
python /reddit-karma-bot-run/run.py