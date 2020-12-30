import pyfiglet
import sys
from logs.logger import log
from config import config_menu
from libs import urwide
import bot

# This is the description of the actual interface
CONSOLE_STYLE = """"""
CONSOLE_UI = """\
Hdr Header    args:#header
---
Txt Status: stopped                     args:#status
===

GFl
Btn [Start]                       #start &press=started
Btn [Config]                         &press=config
Btn [Exit]                          &press=exit
End
"""

# add when working: Btn [Log]                         &press=log

# This is the handling code, providing the logic
class Handler(urwide.Handler):
    def onStarted( self, button ):
        if self.ui.widgets.status.text == "Status: stopped":
            bot.run()
            self.ui.widgets.status.set_text("Status: started")
        else:
            self.ui.widgets.status.set_text("Status: stopped")
    def onConfig( self, button ):
        config_menu.run()

    def onExit( self, button ):
        self.ui.end("Exit")
        log.info("Exiting Karma Bot Menu: Bye! :D")
        sys.exit()

# We create a console application
ui = urwide.Console()
ui.create(CONSOLE_STYLE, CONSOLE_UI, Handler())
ui.widgets.header.set_text("Reddit Karma Farming Bot")

# bring this back later pyfiglet.figlet_format("Reddit Karma Farming Bot", font="slant")

def run():
    ui.main()

if __name__ == "__main__":
    run()
