from utils import prefer_envar
from pathlib import Path
from logs.logger import log
from common_config import SRC_ROOT
import os

BASE_DIR = os.path.join(SRC_ROOT, 'bots/reddit/actions/comments')
DB_DIR = os.path.join(BASE_DIR, "brains")
MAIN_DB = os.path.join(DB_DIR, "brain.db")

CONFIG = prefer_envar({
  # cobe config
  "cobe_base_dir": BASE_DIR,
  "cobe_db_dir": DB_DIR,
  "cobe_main_db": MAIN_DB,
  "cobe_min_db_size":"50mb",
  "cobe_max_db_size":"300mb",
})

log.info(CONFIG)