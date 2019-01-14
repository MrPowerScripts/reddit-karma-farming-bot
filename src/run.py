import reddit
import time
import os
from utils import bytesto, countdown, prob, MAIN_DB
from learn import learn
from logger import log
from requests import get

try:
  ip = get('https://api.ipify.org').text
  print 'My public IP address is:', ip
except Exception as e:
  print "counld not check external ip"

        
limit = 52428800
log.info('------------new bot run--------------')
log.info("user is " + str(reddit.api.user.me()))

if __name__ == '__main__':

    log.info('db size size to start replying:' + str(bytesto(limit, 'm')))
    while True:

      if os.path.isfile(MAIN_DB):
        size = os.path.getsize(MAIN_DB)
        log.info('db size: ' + str(bytesto(size, 'm')))
      else:
        size = 0
      
      if size < limit: # learn faster early on
        log.info('fast learning')
        learn()
        try:
          log.info('new db size: ' + str(bytesto(os.path.getsize(MAIN_DB), 'm')))
        except:
          pass

        countdown(5)
      
      if size > limit: # once we learn enough start submissions and replies  
        log.info('database size is big enough')

        if prob(0.02): # 2% chance we reply to someone
          reddit.random_reply()

        if prob(0.00): # 1% chance we make a random submission
          log.info('making a submission')
          reddit.random_submission()

        if prob(0.10): #25% chance we'll learn more 
          log.info('going to learn')
          learn()
        # Wait 10 minutes to comment and post because of reddit rate limits
        countdown(1)
      log.info('end main loop')
