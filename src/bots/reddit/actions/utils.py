import random
from apis import reddit_api
from logs.logger import log
from config.reddit.reddit_sub_lists import REDDIT_APPROVED_SUBS
from config.common_config import CONFIG_ROOT

with open(f"{CONFIG_ROOT}/reddit/reddit_avoid_subs.txt", "r") as subfile:
  AVOID_SUBS = subfile.read().splitlines()
  subfile.close()

with open(f"{CONFIG_ROOT}/reddit/reddit_avoid_words.txt", "r") as wordfile:
  AVOID_WORDS = wordfile.read().splitlines()
  wordfile.close()

log.debug(f"avoiding subs: {AVOID_SUBS}")

def get_subreddit(nsfw=False, getsubclass=False):

  # if the subreddit list is being used jut return one from there
  if REDDIT_APPROVED_SUBS:
    log.info(f"picking subreddit from approved list")
    subreddit = reddit_api.subreddit(random.choice(REDDIT_APPROVED_SUBS).strip())
    log.info(f"using subreddit: {subreddit.display_name}")
  else:
    log.info(f"picking a random subreddit")
    # otherwise we'll do some logic to get a random subreddit
    subreddit_ok = False
    while not subreddit_ok:
      subreddit = reddit_api.random_subreddit(nsfw=nsfw)
      log.info(f"checking subreddit: {subreddit.display_name}")
      # make sure the radom sub isn't in the avoid sub list
      # keep searching for a subreddit until it meets this condition
      if subreddit.display_name not in AVOID_SUBS:
        subreddit_ok = True

  if getsubclass:
    return subreddit
  else:
    return subreddit.display_name