import reddit
import time

if __name__ == '__main__':
    while True:
        reddit.random_submission()
        reddit.random_reply()
        # Wait 10 minutes to comment and post because of reddit rate limits
        time.sleep(600)
