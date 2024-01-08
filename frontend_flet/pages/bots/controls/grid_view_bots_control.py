from typing import List
from flet import *
 
from controls.text_button_chattum import TextButtonChattum
from controls.text_field_chattum import TextFieldChattum
from models.bot import Bot


class GridViewBotsControl(UserControl): 
    def __init__(self, bots: List[Bot]):
        super().__init__()
        self.bots = bots
        
        self.text_label = Text(
            'Search',
            style=TextThemeStyle.BODY_SMALL,
            color=colors.BLACK,
        )

        self.search_field = TextFieldChattum(on_change=self.on_search_change)

        self.gridView = GridView(
            expand=1,
            runs_count=4,
            max_extent=420,
            child_aspect_ratio=2.0,
            spacing=10,
            run_spacing=10,
            padding=padding.only(top=5),
        )
 
        for bot in self.bots:
            self.gridView.controls.append(self.create_container(bot))
     
    def build(self):     
        return ListView(
                spacing=5,
                controls=[
                    self.text_label,
                    self.search_field,
                    self.gridView,
                ]
            )
    
    def create_container(self, bot):
        def on_click(e):
            self.page.go(f'/bot/{bot.id}')
            
        return Container(
            width=500,
            height=60,
            border=border.all(1, colors.BLACK12),
            border_radius=border_radius.all(10),
            padding=padding.all(15),
            animate=animation.Animation(200, AnimationCurve.EASE_IN_OUT),
            content=Column(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Text(
                        bot.name,
                        style=TextThemeStyle.HEADLINE_MEDIUM,
                        color=colors.BLACK,
                        weight=FontWeight.BOLD,
                        max_lines=2,
                        overflow=TextOverflow.CLIP,
                    ), 
                    TextButtonChattum(
                        text='Select',
                        on_click=on_click
                    )
                ]
            )
        ) 


    def update_bots(self, bots):
        self.bots = bots
        self.gridView.controls.clear()

        for bot in self.bots:
            self.gridView.controls.append(self.create_container(bot))

        self.update()


    def on_search_change(self, e):
        phrase = e.control.value

        self.gridView.controls.clear()
        for bot in self.bots:
            if phrase.lower() in bot.name.lower():
                self.gridView.controls.append(self.create_container(bot))

        self.update()
        


    

