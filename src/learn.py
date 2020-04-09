#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bot import base_brain, Brain
import random
import reddit
from logger import log
import os
from utils import DB_DIR, MAIN_DB, bytesto, MAIN_DB_MAX_SIZE, SUBREDDIT_LIST, LOG_LEARNED_COMMENTS, DISALLOWED_WORDS


def learn(subreddit=None):
    log.info("trying to learn")

    if os.path.isfile(MAIN_DB):
        size = os.path.getsize(MAIN_DB)
        log.info("db size: " + str(bytesto(size, "m")))
    else:
        size = 0

    if size > MAIN_DB_MAX_SIZE:  # learn faster early on
        log.info("DB size has reached limit: {}".format(bytesto(MAIN_DB_MAX_SIZE, "m")))
        return

    try:
        if subreddit: # learning from a supplied 
          if isinstance(subreddit, str):
            log.info("learning from: " + subreddit)
            sub = reddit.api.subreddit(subreddit)
          else:
            log.info('I have no idea what subreddit you gave me. not going to learn.')
            return
        elif SUBREDDIT_LIST: # learn from one of the filtered subreddits
          sub_name = random.choice(SUBREDDIT_LIST)
          log.info("SUBREDDIT_LIST is active")
          log.info("learning from: {}".format(sub_name))
          sub = reddit.api.subreddit(sub_name)
        else:  # no subreddit supplied, so we learn from a random one
            subok = False
            while subok == False:
                sub = reddit.api.subreddit("random")
                if sub.over18 == False:  # we don't want nsfw sub
                    if (
                        sub.subscribers > 100000
                    ):  # easier to get away with stuff on big subs
                        log.info("found: " + str(sub.display_name))
                        subok = True

        sub_db = "{}/{}.db".format(DB_DIR, str(sub.display_name))
        log.info("active db : {}".format(sub_db))
        sub_brain = Brain(sub_db)

        sub_hot = sub.hot()

        log.info("looping through submissions")

        # Loop through each submission
        for submission in sub_hot:
            log.info("checking submission")
            # Replace the "MoreReplies" with all of the submission replies
            submission.comments.replace_more(limit=0)

            # Get a list of all the comments flattened
            comments = submission.comments.list()

            log.debug("looping through comments")
            # Loop through each comment from the submission
            for comment in comments:
                if len(comment.body) < 240:  # long text tends to turn into noise.
                    log.debug("comment score: {}".format(comment.score))
                    if (
                        comment.score > 20
                    ):  # We only want to learn things people like to hear.
                        if (
                            comment.author != submission.author
                        ):  # We only want to learn comments as an ovserver
                            comment_body = comment.body
                            for dis_word in DISALLOWED_WORDS:
                                if dis_word in comment_body:
                                    comment_body.replace(dis_word, "")
                            if LOG_LEARNED_COMMENTS:
                                log.info(
                                    "learning comment. score: {}; comment: {}".format(
                                        comment.score, comment_body.encode("utf8")
                                    )
                                )
                            base_brain.learn(
                                comment_body.encode("utf8")
                            )  # Tell the bot to learn this comment
                            sub_brain.learn(
                                comment_body.encode("utf8")
                            )  # Tell the bot to learn this comment
                            # else:
                            #     log.info("Did not learn form this comment as it contained a word from the dissallowed word list.")
        log.info("done learning")
    except Exception as e:
        # If any errors occur just print it to the console
        log.info(e, exc_info=True)
