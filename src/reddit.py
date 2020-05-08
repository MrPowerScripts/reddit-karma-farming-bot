#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import praw
import requests
from bs4 import BeautifulSoup

import time
import random
import bot
import os
import json
import glob
import urllib
import datetime
from operator import attrgetter, itemgetter
from logger import log
from learn import learn
from utils import (
    DB_DIR,
    SCORE_THRESHOLD,
    SUBMISSION_SEARCH_TEMPLATE,
    SUBREDDIT_LIST,
    MIN_SCORE,
    subreddit,
    prob,
    lru_cache,
    DAY,
    MINUTE,
    TOP_SUBREDDIT_NUM,
    MAX_CACHE_SIZE,
    NUMBER_DAYS_FOR_POST_TO_BE_OLD,
    get_args
)

args = get_args()

if args.username:
    log.info('using cli args or envars')
    REDDIT_CLIENT_ID=args.clientid
    REDDIT_SECRET=args.secret
    REDDIT_PASSWORD=args.password
    REDDIT_USER_AGENT=args.useragent
    REDDIT_USERNAME=args.username
    
    api = praw.Reddit(
      client_id=REDDIT_CLIENT_ID,
      client_secret=REDDIT_SECRET,
      password=REDDIT_PASSWORD,
      user_agent=REDDIT_USER_AGENT,
      username=REDDIT_USERNAME,
    )
else:
    import settings
    log.info('using settings file')
    REDDIT_CLIENT_ID=settings.REDDIT_CLIENT_ID
    REDDIT_SECRET=settings.REDDIT_SECRET
    REDDIT_PASSWORD=settings.REDDIT_PASSWORD
    REDDIT_USER_AGENT=settings.REDDIT_USER_AGENT
    REDDIT_USERNAME=settings.REDDIT_USERNAME

    api = praw.Reddit(
      client_id=REDDIT_CLIENT_ID,
      client_secret=REDDIT_SECRET,
      password=REDDIT_PASSWORD,
      user_agent=REDDIT_USER_AGENT,
      username=REDDIT_USERNAME,
    )


@lru_cache(timeout=DAY,maxsize = MAX_CACHE_SIZE)
def _pushshift_search(sub, start, end):
    """Search sub-reddit for submissions withing a given time range.

    :param sub: name of the sub-reddit (str)
    :param start: epoch date of start (int)
    :param end: epoch date of end (int)
    :return: iterable of reddit submissions (List[dict])
    """
    url = SUBMISSION_SEARCH_TEMPLATE.format(after=start, before=end, subreddit=sub)
    log.info('pushshift api call: {}'.format(url))
    try:
        response = requests.get(url).json().get("data", [])
        #log.info(response)
        return response
    except Exception as e:
        # unable to get data from pushshift
        return None


@lru_cache(timeout=DAY,maxsize = MAX_CACHE_SIZE)
def get_submissions(start_date, end_date, sub):
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
    
    submissions = []
    new_submissions = []

    while not new_submissions: 

        # get submissions
        new_submissions = _pushshift_search(sub, start_date, end_date)

        # base case
        if submissions and submissions[-1]["created_utc"] >= end_date:
            return submissions
        
        # log.info(len(new_submissions))
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

        start_date = next_start

        # log.info(len(submissions))
        time.sleep(0.25)  # limit the requests a bit, be nice with pushshift API
    return submissions


@lru_cache(timeout=DAY,maxsize = MAX_CACHE_SIZE)
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
    for item in api.redditor(api.user.me().name).new(limit=500):
        if item.score <= SCORE_THRESHOLD:

          if isinstance(item, praw.models.Comment):
            log.info(
                "deleting comment(id={id}, body={body}, score={score}, subreddit={sub}|{sub_id})".format(
                    id=item.id,
                    body=item.body,
                    score=item.score,
                    sub=item.subreddit_name_prefixed,
                    sub_id=item.subreddit_id,
                )
            )
            try:
                item.delete()
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
          else:
            log.info(
                "deleting submission(id={id}, score={score}, subreddit={sub}|{sub_id})".format(
                    id=item.id,
                    score=item.score,
                    sub=item.subreddit_name_prefixed,
                    sub_id=item.subreddit_id,
                )
            )
            try:
                item.delete()
            except praw.exceptions.APIException as e:
                raise e
            except Exception as e:
                log.info(
                    "unable to delete submission(id={id}), skip...\n{error}".format(
                        id=item.id, error=e.message
                    )
                )
            count += 1
            log.info(
                "deleted {number} submission with less than {threshold} vote".format(
                    number=count, threshold=SCORE_THRESHOLD
                )
            )


def shadow_check():
  response = requests.get("https://www.reddit.com/user/{}/about.json".format(REDDIT_USERNAME),  headers = {'User-agent': 'hiiii its {}'.format(REDDIT_USERNAME)}).json()
  if "error" in response:
    if response["error"] == 404:
      log.info("account {} is shadowbanned. poor bot :( shutting down the script...".format(REDDIT_USERNAME))
      sys.exit()
    else:
      log.info(response)
  else:
    log.info("{} is not shadowbanned! We think..".format(REDDIT_USERNAME))


def random_submission():
    log.info("making random submission")
    # Get a random submission from a random subreddit
    END_DATE_PY = datetime.datetime.now() - datetime.timedelta(days=NUMBER_DAYS_FOR_POST_TO_BE_OLD)
    ED = int((END_DATE_PY  - datetime.datetime(1970,1,1)).total_seconds())

    START_DATE_PY = END_DATE_PY - datetime.timedelta(days=1)
    SD = int((START_DATE_PY - datetime.datetime(1970,1,1)).total_seconds())

    log.info(START_DATE_PY)
    log.info(END_DATE_PY)
    log.info(SD)
    log.info(ED)
    DATE_DIFF = ""

    log.info("choosing subreddits")
    if SUBREDDIT_LIST:
      log.info('using SUBREDDIT_LIST: {}'.format(SUBREDDIT_LIST))
      subreddits = []
      for subname in SUBREDDIT_LIST:
        subreddits.append(subreddit(
                            name=subname,
                            rank=1,
                            url="https://example.com",
                            subscribers=1000,
                            type="what"))
    else:
      log.info("using get_top_subreddits")
      subreddits = get_top_subreddits()
      #log.info(subreddits)
      
    total_posts = []

    for sub in subreddits[:TOP_SUBREDDIT_NUM]:
        big_upvote_posts = []
        log.info("\n{}\n{}".format("#" * 20, sub))
        tops = get_submissions(SD, ED, sub.name)
        big_upvote_posts = list(filter(lambda item: item["score"] >= MIN_SCORE, tops))
        total_posts += big_upvote_posts
        log.info(
            "found {} posts with score >= {}".format(len(big_upvote_posts), MIN_SCORE)
        )
        del big_upvote_posts

    post_to_repost = random.choice(total_posts)
    # print(post_to_repost)
    # print("doing submission")
    rand_sub = api.submission(id=post_to_repost["id"])

    own_user = api.redditor(REDDIT_USERNAME)
    for submission in own_user.submissions.new(limit=20):
        if submission.title == rand_sub.title:
            log.error("I had posted the post I was just about to make in the last 20 posts, I'm not posting it again.")
            return

    log.info(rand_sub.title)
    #log.info(str(rand_sub))

    # Check if there's any items in the submissions list. If not display error
    if rand_sub:
        try:
            # Check if the we're reposting a selfpost or a link post.
            # Set the required params accodingly, and reuse the content
            # from the old post
            log.info("submission title: " + rand_sub.title)
            log.info("posting to: {}".format(rand_sub.subreddit.name))
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
    if SUBREDDIT_LIST:
      subreddit = random.choice(SUBREDDIT_LIST)
      submission = random.choice(list(api.subreddit(subreddit).hot()))
    else:
      submission = random.choice(list(api.subreddit("all").hot()))
    
    submission.comments.replace_more(
        limit=0
    )  # Replace the "MoreReplies" with all of the submission replies

    sub_name = submission.subreddit.display_name
    brain = "{}/{}.db".format(DB_DIR, sub_name)
    log.info(brain)
    if not glob.glob(brain):
        learn(sub_name)

    reply_brain = bot.Brain(brain)


    try:
#         if prob(.1): # small chance we advertise
#           content = share()
#           comment = random.choice(submission.comments.list())
#           log.info('sharing - thanks for helping out!')
#           sharing = '{} {}'.format(content['comment'], content['url'])
#           reply = comment.reply(sharing)
#           log.info("Replied to comment: {}".format(comment.body))
#           log.info("Replied with: {}".format(reply))
#           return
        if prob(.35):  # There's a larger chance that we'll reply to a comment.
            log.info("replying to a comment")
            comment = random.choice(submission.comments.list())
            response = reply_brain.reply(comment.body)
            
            # We might not be able to learn enough from the subreddit to reply
            # If we don't, then pull a reply from the general database.
            if "I don't know enough to answer you yet!" in response:
              log.info("I don't know enough from {}, using main brain db to reply".format(sub_name))
              brain = "{}/{}.db".format(DB_DIR, "brain")
              reply_brain = bot.Brain(brain)
              response = reply_brain.reply(comment.body)

            reply = comment.reply(response)
            log.info("Replied to comment: {}".format(comment.body))
            log.info("Replied with: {}".format(response))
        else:
            log.info("replying to a submission")
            # Pass the users comment to chatbrain asking for a reply
            response = reply_brain.reply(submission.title)

            # same as above. nobody will ever see this so it's fine.
            if "I don't know enough to answer you yet!" in response:
              log.info("I don't know enough from {}, using main brain db to reply".format(sub_name))
              brain = "{}/{}.db".format(DB_DIR, "brain")
              reply_brain = bot.Brain(brain)
              response = reply_brain.reply(submission.title)

            submission.reply(response)
            log.info("Replied to Title: {}".format(submission.title))
            log.info("Replied with: {}".format(response))
    except praw.exceptions.APIException as e:
        raise e
    except Exception as e:
        log.error(e, exc_info=False)

def share():
  RH_DB = os.path.join(DB_DIR, "rh.json")
  try:
    if os.path.isfile(RH_DB):
      # delete the rh db if it's older than 1 day
      age = int(1)*86400
      now = time.time()
      modified = os.stat(RH_DB).st_mtime
      if modified < now - age:
        if os.path.isfile(RH_DB):
          os.remove(RH_DB)
          log.info('Deleted: %s (%s)' % (file, modified))
    if not os.path.isfile(RH_DB):
      urllib.urlretrieve("https://reviewhuntr.com/api-bait.json", RH_DB)
  except Exception as e:
    log.info("couldn't get bait")
    log.info(e)
    return

  with open(RH_DB) as json_file:
    log.info("chumming the water")
    reviews = json.loads(json_file.read())
    review = random.choice(reviews)
    review['comment'] = random.choice([
      "this is totally urelated but you might enjoy it ",
      "so random but check this out ",
      "somebody is going to fall for this ",
      "don't mind me just sharing this real quick "])
    json_file.close()
  return review
