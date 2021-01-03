import os
import sys
import json
import menu
import pathlib
from utils import prefer_envar
from libs import urwide
from .common_config import SRC_ROOT

CONFIG_JSON_FILE = os.path.join(SRC_ROOT, "config/config.json")

if os.path.isfile(CONFIG_JSON_FILE):
  with open(CONFIG_JSON_FILE, "r") as config_json:
    config_data = prefer_envar(json.load(config_json))
else:
  config_data = prefer_envar({
    "reddit_client_id":"",
    "reddit_client_secret":"",
    "reddit_username":"",
    "reddit_password":"",
  })

CONSOLE_STYLE = """"""

CONSOLE_UI = f'''\
Hdr Reddit Karma Bot Settings
---
Edt   Client ID          [{config_data["reddit_client_id"]}]          #clientid
Edt   Secret            [{config_data["reddit_client_secret"]}]    #secret
---
Edt   Username       [{config_data["reddit_username"]}]               #user
Edt   Password       [{config_data["reddit_password"]}]               #password
===
GFl
Btn [Cancel]                        #btn_cancel &press=cancel
Btn [Save]                          #btn_save   &press=save
End
'''

# Event handler
class Handler(urwide.Handler):

  def onSave( self, button ):
    self.ui.info("Saving")
    fields = self.ui.widgets
    
    config_data["reddit_client_id"] = fields.clientid.edit_text
    config_data["reddit_client_secret"] = fields.secret.edit_text
    config_data["reddit_username"] = fields.user.edit_text
    config_data["reddit_password"] = fields.password.edit_text

    with open(CONFIG_JSON_FILE, "w+") as config_file:
      config_file.write(json.dumps(config_data, indent=4, sort_keys=True))
      config_file.close()
    
    menu.run()


  def onCancel( self, button ):
    self.ui.info("Cancel")
    menu.run()

ui = urwide.Console()
ui.create(CONSOLE_STYLE, CONSOLE_UI, Handler())

# Main
def run():
  ui.main()

if __name__ == "__main__":
  run()


# EOF
