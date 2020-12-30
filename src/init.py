import sys
import bot

if __name__ == "__main__":
  try:
    bot.run()
  except KeyboardInterrupt:
    # quit
    sys.exit()
