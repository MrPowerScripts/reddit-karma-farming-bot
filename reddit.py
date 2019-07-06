#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding("utf8")
from cobe.brain import Brain

import praw
import requests
from bs4 import BeautifulSoup

import time
import random
import os
import glob
import datetime
from operator import attrgetter, itemgetter
from logger import log
from learn import learn
from utils import (
    SCORE_THRESHOLD,
    SUBMISSION_SEARCH_TEMPLATE,
    MIN_SCORE,
    subreddit,
    prob,
    lru_cache,
    DAY,
    TOP_SUBREDDIT_NUM, MAIN_DB
)

api = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_SECRET"),
    password=os.environ.get("REDDIT_PASSWORD"),
    user_agent=os.environ.get("REDDIT_USER_AGENT"),
    username=os.environ.get("REDDIT_USERNAME"),
)
uname = str(api.user.me())
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = ROOT_DIR + "/brains"
MAIN_DB = DB_DIR + '/' + uname + "/brain.db"
try:
    os.mkdir("brains/" + uname)
except:
    pass




@lru_cache(timeout=DAY)
def _pushshift_search(sub, start, end):
    """Search sub-reddit for submissions withing a given time range.

    :param sub: name of the sub-reddit (str)
    :param start: epoch date of start (int)
    :param end: epoch date of end (int)
    :return: iterable of reddit submissions (List[dict])
    """
    url = SUBMISSION_SEARCH_TEMPLATE.format(after=start, before=end, subreddit=sub)
    try:
        return requests.get(url).json().get("data", [])
    except Exception as e:
        # unable to get data from pushshift
        return None


@lru_cache(timeout=DAY)
def get_submissions(start_date, end_date, sub, submissions=[]):
    """'Paginate' function to retrieve all of the submissions
    between a given interval.
    By default pushshift.io only returns maximum of 500 items,
    we need to paginate by using the last retrieved item's date
    as the next start date.
    This is a recursive function.

    :param start_date: epoch of the start date (int)
    :param end_date: epoch of the end date (int)
    :param sub: subreddit to search (str)
    :param submissions: collected submissions (List[dict])
    :return: submissions, sorted by the created date in ascending order (List[dict])
    """
    # base case
    if submissions and submissions[-1]["created_utc"] >= end_date:
        return submissions

    # get submissions
    new_submissions = _pushshift_search(sub, start_date, end_date)
    if not new_submissions:
        return submissions
    # 'paginate', use the last retrieved item's created date
    # for the next request's start date
    next_start = sorted(new_submissions, key=itemgetter("created_utc"))[-1][
        "created_utc"
    ]
    submissions += new_submissions
    # we got all in the interval
    if next_start == start_date:
        return submissions
    time.sleep(0.25)  # limit the requests a bit, be nice with pushshift API
    return get_submissions(next_start, end_date, sub, submissions)


@lru_cache(timeout=DAY)
def get_top_subreddits(min_subscribers=500000):
    """Scraper for redditlist.com.
    Retrieves top subreddits with at least `min_subscribers`.

    :param min_subscribers: filter for subreddits (int)
    :return: list of subreddits with at least `min_subscribers` (List[Subreddit])
    """
    pagination_template = "/?page={}"
    url = "http://www.redditlist.com{page}"
    subs = []
    page = 1
    while True:
        source_code = requests.get(url.format(page=pagination_template.format(page)))
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        listings = soup.findAll(
            "div", attrs={"class": "span4 listing"}
        )  # subscriber list is the middle one
        items = listings[1].findAll("div", {"class": "listing-item"})
        for sub in items:
            attrs = sub.attrs
            num_subscribers = int(
                sub.find("span", {"class": "listing-stat"}).get_text().replace(",", "")
            )
            if num_subscribers < min_subscribers:
                return sorted(subs, key=attrgetter("rank"))
            subs.append(
                subreddit(
                    name=attrs["data-target-subreddit"],
                    rank=int(sub.find("span", {"class": "rank-value"}).get_text()),
                    url=sub.find("span", {"class": "subreddit-url"})
                        .find("a")
                        .get("href"),
                    subscribers=num_subscribers,
                    type=attrs["data-target-filter"],
                )
            )
        page += 1


def submission_timespan():
    # Get the current epoch time, and then subtract one year
    year_ago = int(time.time()) - 31622400
    # Add a day to the time from a year ago
    end_search = year_ago + 86400
    # Return a tuple with the start/end times to search old submissions
    return year_ago, end_search


def delete_comments():
    count = 0
    for comment in api.redditor(api.user.me().name).new(limit=500):
        if comment.score <= SCORE_THRESHOLD:
            log.info(
                "deleting comment(id={id}, body={body}, score={score}, subreddit={sub}|{sub_id})".format(
                    id=comment.id,
                    body=comment.body,
                    score=comment.score,
                    sub=comment.subreddit_name_prefixed,
                    sub_id=comment.subreddit_id,
                )
            )
            try:
                comment.delete()
            except praw.exceptions.APIException as e:
                raise e
            except Exception as e:
                log.info(
                    "unable to delete comment(id={id}), skip...\n{error}".format(
                        id=comment.id, error=e.message
                    )
                )
            count += 1
    log.info(
        "deleted {number} comments with less than {threshold} vote".format(
            number=count, threshold=SCORE_THRESHOLD
        )
    )


def random_submission():
    log.info("making random submission")
    # Get a random submission from a random subreddit
    END_DATE_PY = datetime.datetime.now() - datetime.timedelta(days=364)
    ED = END_DATE_PY.strftime("%s")

    START_DATE_PY = END_DATE_PY - datetime.timedelta(days=1)
    SD = START_DATE_PY.strftime("%s")

    log.info(START_DATE_PY)
    log.info(END_DATE_PY)
    log.info(SD)
    log.info(ED)
    DATE_DIFF = ""
    subreddits = get_top_subreddits()
    for sub in subreddits[:TOP_SUBREDDIT_NUM]:
        log.info("\n{}\n{}".format("#" * 20, sub))
        tops = get_submissions(SD, ED, sub.name)
        big_upvote_posts = list(filter(lambda item: item["score"] >= MIN_SCORE, tops))
        log.info(
            "found {} posts with score >= {}".format(len(big_upvote_posts), MIN_SCORE)
        )

    log.info(big_upvote_posts[0])

    rand_sub = api.submission(id=big_upvote_posts[0])

    subok = False
    while subok == False:
        rand_sub = api.subreddit("all").random()
        if rand_sub.subreddit.over18 == False:  # we don't want nsfw sub
            if (
                rand_sub.subreddit.subscribers > 100000
            ):  # easier to get away with stuff on big subs
                log.info("posting to: " + rand_sub.subreddit.display_name)
                subok = True

    # Check if there's any items in the submissions list. If not display error
    if rand_sub:
        try:
            # Check if the we're reposting a selfpost or a link post.
            # Set the required params accodingly, and reuse the content
            # from the old post
            log.info("submission title: " + rand_sub.title)
            log.info("tokenizing title")
            if rand_sub.is_self:
                params = {"title": rand_sub.title, "selftext": rand_sub.selftext}
            else:
                params = {"title": rand_sub.title, "url": rand_sub.url}

            # Submit the same content to the same subreddit. Prepare your salt picks
            api.subreddit(rand_sub.subreddit.display_name).submit(**params)
        except praw.exceptions.APIException as e:
            raise e
        except Exception as e:
            log.info(e)
    else:
        log.error("something broke")


def random_reply():
    log.info("making random reply")
    # Choose a random submission from /r/all that is currently hot
    submission = random.choice(list(api.subreddit("all").hot()))
    submission.comments.replace_more(
        limit=0
    )  # Replace the "MoreReplies" with all of the submission replies

    sub_name = submission.subreddit.display_name
    brain = "{}/" + api.user.me() + "/{}.db".format(DB_DIR, sub_name)
    if not glob.glob(brain):
        learn(str(api.user.me()), sub_name)
    log.info("Main database: {}".format(MAIN_DB))

    reply_brain = Brain(brain)

    try:
        if prob(.35):  # There's a larger chance that we'll reply to a comment.
            log.info("replying to a comment")
            comment = random.choice(submission.comments.list())
            response = reply_brain.reply(comment.body)
            reply = comment.reply(response)
            log.info("Replied to comment: {}".format(comment))
            log.info("Replied with: {}".format(reply))
        else:
            log.info("replying to a submission")
            # Pass the users comment to chatbrain asking for a reply
            response = reply_brain.reply(submission.title)
            submission.reply(response)
            log.info("Replied to Title: {}".format(submission.title))
            log.info("Replied with: {}".format(response))
    except praw.exceptions.APIException as e:
        raise e
    except Exception as e:
        log.error(e, exc_info=False)
