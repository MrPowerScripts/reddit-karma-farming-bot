import os
import collections
import random
import time
import yaml
import string
from config.common_config import ENVAR_PREFIX
from logs.logger import log

def random_string(length: int) -> str:
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for i in range(length))  

def get_current_epoch() -> int:
  return int(time.time())

def prefer_envar(configs: dict) -> dict:
  for config in list(configs):
    config_envar = f"{ENVAR_PREFIX}{config}".upper()
    if os.environ.get(config_envar):
      log.info(f"loading {config_envar} from envar. Value: {configs[config]}")
      configs[config]=os.environ.get(config_envar)
    else:
      log.debug(f"no environment config for: {config_envar}")
  
  return configs

def load_config(config: str):
  with open(f"{os.path.join(os.path.dirname(__file__))}/config/{config}.yml") as file:
    return yaml.load(file, Loader=yaml.FullLoader)

def convert_size_to_bytes(size_str: str):
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
      'terabyte':  1024 ** 4,
      'petabyte':  1024 ** 5,
      'exabyte':   1024 ** 6,
      'zetabyte':  1024 ** 7,
      'yottabyte': 1024 ** 8,
      'kb': 1024,
      'mb': 1024**2,
      'gb': 1024**3,
      'tb': 1024**4,
      'pb': 1024**5,
      'eb': 1024**6,
      'zb': 1024**7,
      'yb': 1024**8,
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

def check_internet(host="1.1.1.1", port=53, timeout=5):
    """
    Host: 1.1.1.1 (cloudflare DNS)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        log.error(ex.message)
        return False


def get_seconds_to_wait(ex_msg=None):
    try:
        msg = ex_msg.lower()
        search = re.search(r"\b(minutes)\b", msg)
        # I found out that if the message said 3 minute
        # it could be 3 minute 20 seconds, so to be safe and avoid another exception,
        # we wait a full extra minute
        minutes = int(msg[search.start() - 2]) + 1
        return minutes * 60
    except:
        return 60


def get_public_ip():
    try:
        for service in ["https://api.ipify.org", "http://ip.42.pl/raw"]:
            external_ip = get(service).text
            if external_ip:
                return external_ip
    except Exception as e:
        # try one more before giving up
        try:
            return get("http://httpbin.org/ip").json()["origin"].split(",")[0]
        except:
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


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

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
        'terabyte':  1024 ** 4,
        'petabyte':  1024 ** 5,
        'exabyte':   1024 ** 6,
        'zetabyte':  1024 ** 7,
        'yottabyte': 1024 ** 8,
        'kb': 1024,
        'mb': 1024**2,
        'gb': 1024**3,
        'tb': 1024**4,
        'pb': 1024**5,
        'eb': 1024**6,
        'zb': 1024**7,
        'yb': 1024**8,
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
