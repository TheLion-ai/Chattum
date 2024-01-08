from typing import List
from flet import *

from backend_controller import get_bots 
from models.bot import Bot
from pages.bots.controls.create_new_bot_control import CreateNewBotControl
from pages.bots.controls.grid_view_bots_control import GridViewBotsControl


class BotsView(View):
    def __init__(self):
        super().__init__(
            route="/bots",
            bgcolor = colors.WHITE10,
            scroll = ScrollMode.ALWAYS,  
            controls = [
                BotsPage(),
            ]
        )
    

class BotsPage(UserControl):
    def __init__(self):
        super().__init__()
        self.bots = [Bot(bot) for bot in get_bots()] 
        self.create_new_bot_control = CreateNewBotControl(get_bots_fn=self.get_bots_from_server)
        self.grid_view_bots_control = GridViewBotsControl(bots=self.bots)
 

    def build(self):
        return Container(
            padding = padding.symmetric(horizontal=40, vertical=60),
            content = Column(
                controls=[
                    self.create_new_bot_control, 
                    self.grid_view_bots_control,
                ]
            ),
        )
 
    
    def get_bots_from_server(self) -> List[Bot]:
        self.bots = [Bot(bot) for bot in get_bots()]
        self.grid_view_bots_control.update_bots(bots=self.bots)


 