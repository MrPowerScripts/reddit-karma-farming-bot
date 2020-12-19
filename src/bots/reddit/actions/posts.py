from apis.pushshift import PushShift
from actions import Action

class Posts(Action):
  def __init__(self):
    self.psapi = PushShift()

  def action(self):
    self.psapi.get_posts("pcmasterrace")