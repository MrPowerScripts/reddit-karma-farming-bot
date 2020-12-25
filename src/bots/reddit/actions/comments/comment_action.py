from actions import Action

class Comments(Action):
  def __init__(self, source='cobe'):
    self.source = importlib.import_module(f"sources.{source}")

  def init(self):
    self.ready = False
    self.source.init()
    self.ready = True

  def action(self):
    print('lol')

  def get_comment(self, respond_to=""):
    if self.ready:
      # get the comment 
      pass
    else:
      #not ready to get a comment
      pass


