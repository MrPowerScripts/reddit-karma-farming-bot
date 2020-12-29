import urwide
import os
import sys
import json
import menu


CONSOLE_STYLE = """"""

CONSOLE_UI = """\
Hdr Reddit Karma Bot Settings
---
Edt   Client ID          []          #clientid
Edt   Secret            []    #secret
---
Edt   Username       []               #user
Edt   Password       []               #password
===
GFl
Btn [Cancel]                        #btn_cancel &press=cancel
Btn [Save]                          #btn_save   &press=save
End
"""

# Event handler
class Handler(urwide.Handler):

	def onSave( self, button ):
		self.ui.info("Saving")
		fields = self.ui.widgets
		f = open("config/config.json", "w")
		filedata = {
  		"reddit_client_id":"",
  		"reddit_client_secret":"",
  		"reddit_username":"",
  		"reddit_password":"",
		}
		filedata["reddit_client_id"] = fields.clientid.edit_text
		filedata["reddit_client_secret"] = fields.secret.edit_text
		filedata["reddit_username"] = fields.user.edit_text
		filedata["reddit_password"] = fields.password.edit_text
		f.write(json.dumps(filedata))
		f.close()
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
