from bot import brain
import reddit
import time


if __name__ == '__main__':

    # Start an endless loop
    while True:

        # Wrap everything in a try/except
        # so that it doesn't stop because of errors
        try:
            # Get the hot submissions from a random subreddit
            submissions = reddit.api.subreddit('random').hot()

            # Loop through each submission
            for submission in submissions:

                # Replace the "MoreReplies" with all of the submission replies
                submission.comments.replace_more(limit=0)

                # Get a list of all the comments flattened
                comments = submission.comments.list()

                # Loop through each comment from the submission
                for comment in comments:

                    # Tell the bot to learn this comment
                    brain.learn(comment.body.encode('utf8'))
        except Exception as e:
            # If any errors occur just print it to the console
            print e

        # Wait 15 seconds and study a different subreddit
        time.sleep(15)
