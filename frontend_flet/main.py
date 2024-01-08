from flet import *

from pages.bot.bot_view import BotView
from pages.bots.bots_view import BotsView 



class ChattumApp(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.on_route_change = self.route_change
        self.page.update()

    def build(self):
        self.layout = ProgressRing()
        return self.layout
    
    def initialize(self):
        self.page.go("/bots") 

    def route_change(self, e): 
        troute = TemplateRoute(self.page.route)
        if troute.match("/bots"): 
            self.page.views.append(BotsView())
        elif troute.match("/bot/:bot_id"):
            self.page.views.append(BotView(troute.bot_id))
        else: 
            # TODO: 404, this page doesnt exist or sth
            pass

        self.page.update() 


if __name__ == "__main__":
    def main(page: Page):
        page.title = "Chattum"
        page.padding = 0
        page.bgcolor = colors.WHITE10
        page.scroll = ScrollMode.ALWAYS


        # btn = ElevatedButton("Toast")
        # page.add(btn)
        # Toast(
        #     page,
        #     icons.PERSON_SHARP,
        #     "Toast title",
        #     "Toast description",
        #     btn,
        #     colors.RED,
        # ).struct()

        app = ChattumApp(page)
        page.add(app)
        page.update()
        app.initialize() 

    app(target=main, assets_dir="assets", view=WEB_BROWSER)
