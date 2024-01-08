from flet import *

from backend_controller import get_bot
from models.bot import Bot 
from pages.bot.controls.sidebar import Sidebar 


class BotView(View):
    def __init__(self, bot_id: str):
        super().__init__(
            route="/bot",
            bgcolor = colors.WHITE10, 
            padding=0,
            controls = [
                BotPage(Bot(get_bot(bot_id)))
            ]
        )
 
    

class BotPage(UserControl):
    def __init__(self, bot: Bot):
        super().__init__(
            expand=True,
        ) 
        self.bot = bot

        self.text_label = Text(
            self.bot.id,
            style=TextThemeStyle.BODY_SMALL,
            color=colors.BLACK,
        )

    def build(self):
        return Container( 
            expand=True, 
            content=Sidebar(),
            # content = Row(
            #     controls=[
            #         Sidebar(),
            #         Column(
            #             expand = True,
            #             alignment = MainAxisAlignment.CENTER,
            #             horizontal_alignment = CrossAxisAlignment.CENTER,
            #             controls=[
            #                 Text(
            #                     'text',
            #                     style=TextThemeStyle.BODY_SMALL,
            #                     color=colors.BLACK,
            #                 )
            #             ]
            #         )
            #     ]
            # )
        )
    