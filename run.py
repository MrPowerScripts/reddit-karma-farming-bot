#!/usr/bin/env python
# -*- coding: utf-8 -*-

import praw
import reddit
from reddit import MAIN_DB
import os
from utils import (
    bytesto,
    countdown,
    prob,
    PROBABILITIES,
    check_internet,
    MAIN_DB_MIN_SIZE,
    get_seconds_to_wait,
    reddit_bot_action,
    get_current_epoch, get_unused_proxy, release_proxy
)
from learn import learn
from logger import log
import requests
import sys
import gc

args = sys.argv

ip = args[1]
port = args[2]
proxy_url = 'http://' + ip + ':' + port
proxy_d = {'http': proxy_url}
proxy = get_unused_proxy(proxy_d)
try:
    r = requests.get("https://jsonip.com/")
    ip = r.json()['ip']
    log.info("My public IP address is: {}".format(ip))
except Exception as e:
    log.error("could not check external ip")

RATE_LIMIT = 0
NEED_TO_WAIT = 0
log.info("------------new bot run--------------")
log.info("user is " + str(reddit.api.user.me()))

reddit_bot = [
    reddit_bot_action("reply", reddit.random_reply, PROBABILITIES["REPLY"], 0),
    reddit_bot_action(
        "submit", reddit.random_submission, PROBABILITIES["SUBMISSION"], 0
    ),
    reddit_bot_action("delete", reddit.delete_comments, PROBABILITIES["DELETE"], 0),
]

if __name__ == "__main__":
    log.info("db size size to start replying:" + str(bytesto(MAIN_DB_MIN_SIZE, "m")))
    while True:

        if os.path.isfile(MAIN_DB):
            size = os.path.getsize(MAIN_DB)
            log.info("db size: " + str(bytesto(size, "m")))
        else:
            size = 0

        if size < MAIN_DB_MIN_SIZE:  # learn faster early on
            log.info("fast learning")
            # set the proxy
            learn(str(reddit.api.user.me()))
            # release the proxy
            try:
                log.info("new db size: " + str(bytesto(os.path.getsize(MAIN_DB), "m")))
            except:
                pass

            countdown(5)

        if (
            size > MAIN_DB_MIN_SIZE
        ):  # once we learn enough start submissions and replies
            log.info("database size is big enough")

            for action in reddit_bot:
                if action.rate_limit_unlock_epoch != 0:
                    if action.rate_limit_unlock_epoch > get_current_epoch():
                        log.info(
                            "{} hit RateLimit recently we need to wait {} seconds with this".format(
                                action.name,
                                action.rate_limit_unlock_epoch - get_current_epoch(),
                            )
                        )
                        continue
                    else:
                        action._replace(rate_limit_unlock_epoch=0)
                else:
                    if prob(action.probability):
                        log.info("making a random {}".format(action.name))
                        try:
                            action.action()
                        except praw.exceptions.APIException as e:
                            log.error(
                                "something weird happened, {}".format(e), exc_info=False
                            )
                            secs_to_wait = get_seconds_to_wait(str(e))
                            action._replace(
                                rate_limit_unlock_epoch=(
                                    get_current_epoch() + secs_to_wait
                                )
                            )
                            log.info(
                                "{} hit RateLimit, need to sleep for {} seconds".format(
                                    action.name, secs_to_wait
                                )
                            )
                        except Exception as e:
                            log.error(
                                "something weird happened, {}".format(e), exc_info=False
                            )
            if prob(PROBABILITIES["LEARN"]):  # chance we'll learn more
                log.info("going to learn")

                # set  proxy
                learn(str(reddit.api.user.me()))
                # release the proxy

            # Wait 10 minutes to comment and post because of reddit rate limits
            countdown(1)
        log.info("end of sleep")
        log.info("end main loop")
        num = gc.collect()
        print("Collecting Memory "+str(num))

