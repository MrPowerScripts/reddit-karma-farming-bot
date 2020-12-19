from cobe.brain import Brain
from utils import MAIN_DB

base_brain = Brain(MAIN_DB)

class Cobe():
  def __init__(self, min_db, max_db):
    self.min_db = min_db
    self.max_db = max_db

  def init()