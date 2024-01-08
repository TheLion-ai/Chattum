from flet import *
 
 
class Sidebar(UserControl):
    def __init__(self):
        super().__init__()
        self._min_width = 40
        self._max_width = 350 

    def build(self):
        self.arrow_button = IconButton(
            icon=icons.KEYBOARD_ARROW_RIGHT,
            selected_icon=icons.CLOSE,
            on_click=self._arrow_button_pressed,
            icon_size=18,
            selected=False,
            style=ButtonStyle(color=colors.BLACK),
        )

        self.buttons = Container(
            border=border.all(1, colors.BLACK12),
            visible=False,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                expand=True,
                scroll=ScrollMode.AUTO,
                controls=[
                    Text(
                        'Bot name',
                        style=TextThemeStyle.BODY_SMALL,
                        color=colors.BLACK,
                    ) ,
                    Text(
                        'Bot nameBot name',
                        style=TextThemeStyle.BODY_SMALL,
                        color=colors.BLACK,
                    ) ,
                    Text(
                        'Bot name',
                        style=TextThemeStyle.BODY_SMALL,
                        color=colors.BLACK,
                    ) ,
                    Text(
                        'Bot name',
                        style=TextThemeStyle.BODY_SMALL,
                        color=colors.BLACK,
                    ) ,
                ]
            )
        )

        self.view = Container(
            width=self._min_width, 
            animate=animation.Animation(200, AnimationCurve.EASE_IN_OUT), 
            on_animation_end=lambda e: self.buttons.update(),
            bgcolor=colors.BLACK12, 
            top=0,
            bottom=0,
            content = Column(
                expand=True,
                controls = [
                    Row(
                        height=40,
                        alignment = MainAxisAlignment.END,
                        controls = [
                            self.arrow_button,
                        ]
                    ),
                    self.buttons
                ]
            )
        )

        return self.view

    def _arrow_button_pressed(self, e):
        self._animate(e)
        e.control.selected = not e.control.selected
        e.control.update()
        self.buttons.visible = not self.buttons.visible 
        if self.buttons.visible == False:
            self.buttons.update()

    def _animate(self, e): 
        self.view.width = self._min_width if self.view.width == self._max_width else self._max_width
        self.view.update()