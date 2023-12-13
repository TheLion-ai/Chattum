from typing import List
from flet import *

from backend_controller import create_new_bot, get_bots
from controls.text_button_chattum import TextButtonChattum
from controls.text_field_chattum import TextFieldChattum
from models.bot import Bot


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



class CreateNewBotControl(UserControl): 
    def __init__(self, get_bots_fn):
        super().__init__()

        self.get_bots = get_bots_fn
        
        self.text_label = Text(
            'Bot name',
            style=TextThemeStyle.BODY_SMALL,
            color=colors.BLACK,
        )
        self.text_field_name = TextFieldChattum()
        self.text_button_create = TextButtonChattum(
            text='Create',
            on_click=self.create_button_pressed,
        )

        self.c = Container(
            width=400,
            height=45,
            border=border.all(1, colors.BLACK12),
            border_radius=border_radius.all(10),
            padding=padding.only(left=10, right=10, top=2),
            animate=animation.Animation(200, AnimationCurve.EASE_IN_OUT),
            content=Column(
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.START,
                controls=[
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Text(
                                'Create a new bot', 
                                style=TextThemeStyle.BODY_SMALL, 
                                color=colors.BLACK
                            ),
                            IconButton(
                                icon=icons.KEYBOARD_ARROW_DOWN,
                                selected_icon=icons.KEYBOARD_ARROW_UP,
                                on_click=self.arrow_button_pressed,
                                icon_size=18,
                                selected=False,
                                style=ButtonStyle(color=colors.BLACK),
                            )
                        ]
                    ),
                    self.text_label,
                    self.text_field_name,
                    self.text_button_create,
                ]
            )
        )
     
    def animate(self, e): 
        self.c.height = 45 if self.c.height == 180 else 180
        self.c.update()

    def arrow_button_pressed(self, e):
        self.animate(e)
        e.control.selected = not e.control.selected
        e.control.update()

    def create_button_pressed(self, e):
        create_new_bot(bot_name=self.text_field_name.value)
        self.get_bots()
        e.control.update()

    def build(self):
        return self.c
    


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
        # return self.gridView
      
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
            self.page.go(f'/bot_menu/{bot.id}')
            
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
        


    

