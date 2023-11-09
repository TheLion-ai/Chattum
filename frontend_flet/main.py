import flet
from flet import (  
    ElevatedButton, 
    Page, 
    TemplateRoute,
    ProgressRing, 
    UserControl,
    View,
    colors,  
)

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
        # TODO: some async work
        self.page.go("/") 

    def route_change(self, e): 
        troute = TemplateRoute(self.page.route) 
        if troute.match("/"): 
            self.page.views.append(
                    View(
                        "/",
                        [ 
                            ElevatedButton("Go Store", on_click=lambda _: self.page.go("/store")),
                        ],
                    )
                )
        elif troute.match("/store"): 
            self.page.views.append(
                    View(
                        "/store",
                        [ 
                            ElevatedButton("Go Home", on_click=lambda _: self.page.go("/")),
                        ],
                    )
                ) 
        self.page.update() 

if __name__ == "__main__":
    def main(page: Page):
        page.title = "Chattum"
        page.padding = 0
        page.bgcolor = colors.WHITE70
        app = ChattumApp(page)
        page.add(app)
        page.update()
        app.initialize() 

    flet.app(target=main, view=flet.WEB_BROWSER)
