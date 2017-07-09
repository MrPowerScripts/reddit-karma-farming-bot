import praw
import time
import random
import bot
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


def random_submission():
    # Get submissions from a random subreddit one year ago
    submissions = list(api.subreddit('random').submissions(
        *submission_timespan()))

    # Check if there's any items in the submissions list. If not display error
    if submissions:
        # If we get more than one submission choose a random one from the list
        if len(submissions) > 1:
            chosen = random.choice(submissions)
        else:
            chosen = submissions[0]

        try:
            # Check if the we're reposting a selfpost or a link post.
            # Set the required params accodingly, and reuse the content
            # from the old post
            if chosen.is_self:
                params = {"title":chosen.title, "selftext":chosen.selftext}
            else:
                params = {"title":chosen.title, "url":chosen.url}

            # Submit the same content to the same subreddit. Prepare your salt picks
            api.subreddit(chosen.subreddit.display_name).submit(**params)
        except Exception as e:
            print e

    else:
        print 'list empty - something broke'


def random_reply():
    # Choose a random submission from /r/all that is currently hot
    submission = random.choice(list(api.subreddit('all').hot()))
    # Replace the "MoreReplies" with all of the submission replies
    submission.comments.replace_more(limit=0)

    # Choose a random top level comment
    comment = random.choice(submission.comments.list())

    try:
        # Pass the users comment to chatbrain asking for a reply
        response = bot.brain.reply(comment.body)
    except Exception as e:
        print e

    try:
        # Reply tp the same users comment with chatbrains reply
        reply = comment.reply(response)
    except Exception as e:
        print "reply FAILED"
