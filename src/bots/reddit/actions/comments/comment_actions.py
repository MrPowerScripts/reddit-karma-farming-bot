from actions import Action
from sources.cobe import Cobe
from logs.logger import log

class Comments(Action):
  def __init__(self, source='cobe'):
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

  def action(self):
    print('lol')

  def get_comment(self, respond_to=""):
    if self.ready:
      # get the comment 
      pass
    else:
      #not ready to get a comment
      pass


