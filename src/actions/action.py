class Action():
  def __init__(self):
    self.ready = False

  def _init(self):
    self.ready = True

  def action(self):
    self._init()
    pass