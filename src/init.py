import sys
from logs.logger import log
from utils import check_internet
import bot

if __name__ == "__main__":
    if check_internet() is True:
        try:
            log.info('Internet connection found')
            bot.run()
        except KeyboardInterrupt:
            # quit
            sys.exit()
        else:
            log.info('Please check your internet connection')
            sys.exit()
