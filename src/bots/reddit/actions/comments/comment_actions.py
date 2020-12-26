from .sources.cobe import Cobe
from logs.logger import log
from utils import chance

class Comments():
  def __init__(self, source='cobe'):
    self.ready = False
    self.source = source
    self.cobe = Cobe()

  def init(self):
    log.info("intiializing comments")
    self.ready = False
    if self.source == "cobe":
      log.info("using cobe to generate comments")
      self.cobe.init()
    self.ready = True
    log.info("commenting ready")

  def comment(self, roll=1):
    if not self.ready:
      log.info("comments need to be initialized")
      self.init()

    if chance(roll):
      log.info("would have commented if this was finished")

  def get_comment(self, respond_to=""):
    if self.ready:
      # get the comment 
      pass
    else:
      #not ready to get a comment
      pass


