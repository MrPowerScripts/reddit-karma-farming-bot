import os
import collections
import random
import time
import string
from config.common_config import ENVAR_PREFIX
from logs.logger import log
import urllib.request
## HELPER VARS

DAY = 86400
MONTH = 2678400
YEAR = 31536000


def random_string(length: int) -> str:
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for i in range(length))

def prefer_envar(configs: dict) -> dict:
  for config in list(configs):
    config_envar = f"{ENVAR_PREFIX}{config}".lower()
    if os.environ.get(config_envar):
      configs[config]=os.environ.get(config_envar)
      log.info(f"loading {config_envar} from envar. Value: {configs.get(config)}")
    else:
      log.debug(f"no environment config for: {config_envar}")

  return configs

# Checks if the machine has internet and also can connect to reddit
def check_internet(host="https://reddit.com", timeout=5):
    try:
        urllib.request.urlopen(host, None, timeout)
        return True
    except Exception as ex:
        log.error(ex)
        return False


def get_public_ip():
    try:
        external_ip = urllib.request.urlopen("https://api.ipify.org")
        if external_ip:
            return external_ip.read().decode("utf-8")
    except Exception as e:
        log.error("could not check external ip")


def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
      sample code:
          print('mb= ' + str(bytesto(314575262000000, 'm')))
      sample output:
          mb= 300002347.946
  """

    a = {"k": 1, "m": 2, "g": 3, "t": 4, "p": 5, "e": 6}
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return round(r)


def is_past_one_day(time_to_compare):
    return int(time.time()) - time_to_compare >= DAY


def countdown(seconds=1):
    # log.info("sleeping: " + str(seconds) + " seconds")
    # for i in range(seconds, 0, -1):
    #     # print("\x1b[2K\r" + str(i) + " ")
    #     time.sleep(3)
    # log.info("waking up")
    time.sleep(seconds)


def chance(value=.20):
    rando = random.random()
    # log.info("prob: " + str(value) + " rolled: " + str(rando))
    return rando < value



def tobytes(size_str):
    """Convert human filesizes to bytes.
    https://stackoverflow.com/questions/44307480/convert-size-notation-with-units-100kb-32mb-to-number-of-bytes-in-python
    Special cases:
     - singular units, e.g., "1 byte"
     - byte vs b
     - yottabytes, zetabytes, etc.
     - with & without spaces between & around units.
     - floats ("5.2 mb")
    To reverse this, see hurry.filesize or the Django filesizeformat template
    filter.
    :param size_str: A human-readable string representing a file size, e.g.,
    "22 megabytes".
    :return: The number of bytes represented by the string.
    """
    multipliers = {
        'kilobyte':  1024,
        'megabyte':  1024 ** 2,
        'gigabyte':  1024 ** 3,
        'kb': 1024,
        'mb': 1024**2,
        'gb': 1024**3,
    }

    for suffix in multipliers:
        size_str = size_str.lower().strip().strip('s')
        if size_str.lower().endswith(suffix):
            return int(float(size_str[0:-len(suffix)]) * multipliers[suffix])
    else:
        if size_str.endswith('b'):
            size_str = size_str[0:-1]
        elif size_str.endswith('byte'):
            size_str = size_str[0:-4]
    return int(size_str)
