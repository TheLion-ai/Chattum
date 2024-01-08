from flet import *

from backend_controller import create_new_bot
from controls.text_button_chattum import TextButtonChattum
from controls.text_field_chattum import TextFieldChattum


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
            on_click=self._create_button_pressed,
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
                                on_click=self._arrow_button_pressed,
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
     
    def _animate(self, e): 
        self.c.height = 45 if self.c.height == 180 else 180
        self.c.update()

    def _arrow_button_pressed(self, e):
        self._animate(e)
        e.control.selected = not e.control.selected
        e.control.update()

    def _create_button_pressed(self, e):
        create_new_bot(bot_name=self.text_field_name.value)
        self.get_bots()
        e.control.update()

    def build(self):
        return self.c
    


 
