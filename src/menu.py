import urwide
import pyfiglet
import configmenu
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
Btn [Log]                         &press=log
Btn [Config]                         &press=config
Btn [Exit]                          &press=exit
End
"""

# This is the handling code, providing the logic
class Handler(urwide.Handler):
    def onStarted( self, button ):
        if self.ui.widgets.status.text == "Status: stopped":
            bot.run()
            self.ui.widgets.status.set_text("Status: started")
        else:
            self.ui.widgets.status.set_text("Status: stopped")
    def onConfig( self, button ):
        configmenu.run()
    def onExit( self, button ):
        self.ui.end("Exit")

# We create a console application
ui = urwide.Console()
ui.create(CONSOLE_STYLE, CONSOLE_UI, Handler())
ui.widgets.header.set_text(pyfiglet.figlet_format("Reddit Karma Farming Bot", font="slant"))

def run():
    ui.main()
if __name__ == "__main__":
    run()
