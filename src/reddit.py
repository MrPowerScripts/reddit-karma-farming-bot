import praw
import time
import random
import bot
import os
import glob
import nltk
nltk.download('wordnet')
nltk.download('punkt')
from logger import log
from learn import learn
from nltk.corpus import wordnet as wn
from utils import DB_DIR

SCORE_THRESHOLD = -2

if os.environ.get('REDDIT_CLIENT_ID'):
  api = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                    client_secret=os.environ.get('REDDIT_SECRET'),
                    password=os.environ.get('REDDIT_PASSWORD'),
                    user_agent=os.environ.get('REDDIT_USER_AGENT'),
                    username=os.environ.get('REDDIT_USERNAME'))
else:
  import settings
  api = praw.Reddit(client_id=settings.REDDIT_CLIENT_ID,
                    client_secret=settings.REDDIT_SECRET,
                    password=settings.REDDIT_PASSWORD,
                    user_agent=settings.REDDIT_USER_AGENT,
                    username=settings.REDDIT_USERNAME)

def submission_timespan():
  # Get the current epoch time, and then subtract one year
  year_ago = int(time.time()) - 31622400
  # Add a day to the time from a year ago
  end_search = year_ago + 86400
  # Return a tuple with the start/end times to search old submissions
  return (year_ago, end_search)

def delete_comments():
    count = 0
    for comment in api.redditor(api.user.me().name).new(limit=500):
        if comment.score <= SCORE_THRESHOLD:
            log.info('deleting comment(id={id}, body={body}, score={score}, subreddit={sub}|{sub_id})'.format(
                id=comment.id,
                body=comment.body,
                score=comment.score,
                sub=comment.subreddit_name_prefixed,
                sub_id=comment.subreddit_id))
            comment.delete()
            count += 1
    log.info('deleted {number} comments with less than {threshold} vote'.format(number=score, threshold=SCORE_THRESHOLD))

def random_submission():
  log.info('making random submission')
  # Get a random submission from a random subreddit

  subok = False
  while subok == False:
    rand_sub = api.subreddit('all').random()
    if rand_sub.subreddit.over18 == False: # we don't want nsfw sub
      if rand_sub.subreddit.subscribers > 100000: # easier to get away with stuff on big subs
        log.info("posting to: " + rand_sub.subreddit.display_name)
        subok = True

  # Check if there's any items in the submissions list. If not display error
  if rand_sub:
    try:
      # Check if the we're reposting a selfpost or a link post.
      # Set the required params accodingly, and reuse the content
      # from the old post
      title = rand_sub.title
      log.info("submission title: " + rand_sub.title)
      log.info("tokenizing title")
      for word in nltk.word_tokenize(rand_sub.title):
        log.debug("word: " + word)
        try:
          ss = wn.synsets(word)[0]

          # log.info(ss.pos())
          # log.info(ss.lemma_names()[1])
          if ss.pos() == "v" or ss.pos() == "n" and ss.lemma_names()[1]:
              log.info('editing the title: ' + ss.lemma() + " to " + ss.lemma_names()[1])
              new_title = str.replace(ss.lemma(), ss.lemma_names()[1])
              log.info('{} {}'.format(ss.lemma(), ss.lemma_names()[1]))
          else:
            new_title = title
        except:
          log.debug('no synonym for' + word)
          new_title = title
        
      log.info("new title: " + new_title)
      if rand_sub.is_self:
          params = {"title": new_title, "selftext":rand_sub.selftext}
      else:
          params = {"title": new_title, "url": rand_sub.url}

      # Submit the same content to the same subreddit. Prepare your salt picks
      api.subreddit(rand_sub.subreddit.display_name).submit(**params)
    except Exception as e:
      print e

  else:
    print 'something broke'

def random_reply():
  log.info('making random reply')
  # Choose a random submission from /r/all that is currently hot
  submission = random.choice(list(api.subreddit('all').hot()))

  sub_name = submission.subreddit.display_name
  brain = "{}/{}.db".format(DB_DIR, sub_name)
  if not glob.glob(brain):
    learn(sub_name)

  reply_brain = bot.Brain(brain)
  # Replace the "MoreReplies" with all of the submission replies
  submission.comments.replace_more(limit=0)

  # Choose a random top level comment
  comment = random.choice(submission.comments.list())

  try:
    # Pass the users comment to chatbrain asking for a reply
    response = reply_brain.reply(comment.body)
  except Exception as e:
    log.error(e, exc_info=False)

  try:
    # Reply tp the same users comment with chatbrains reply
    reply = comment.reply(response)
  except Exception as e:
    log.error(e, exc_info=False)
