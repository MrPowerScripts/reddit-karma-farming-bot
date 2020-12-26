from cobe.brain import Brain
from config.cobe_config import CONFIG
from logs.logger import log
from utils import bytesto
import os

class Cobe():
  def __init__(self, config=CONFIG):
    self.config = CONFIG
    self.brain = Brain(self.config.get("cobe_main_db"))
    self.size = 0

  def init(self):
    main_db = self.config.get("cobe_main_db")
    
    if os.path.isfile(main_db):
      self.size = os.path.getsize(main_db)
      log.info("cobe db size: " + str(bytesto(self.size, "m")))
    else:
      size = 0
