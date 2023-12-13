from flet import *

from backend_controller import get_bot
from models.bot import Bot 

class BotMenuView(View):
    def __init__(self, bot_id: str):
        super().__init__()
        self.bot = Bot(get_bot(bot_id))
    
        self.route = "/bot_menu"
        self.bgcolor = colors.WHITE10
        self.padding = padding.symmetric(horizontal=40, vertical=60)
        self.controls = [
            BotMenuPage(self.bot)
        ]
    


class BotMenuPage(UserControl):
    def __init__(self, bot: Bot):
        super().__init__() 
        self.bot = bot

        self.text_label = Text(
            self.bot.id,
            style=TextThemeStyle.BODY_SMALL,
            color=colors.BLACK,
        )

    def build(self):
        return Column(
            controls=[
                self.text_label,
            ]
        )
    
 
