from flet import *

class TextFieldChattum(TextField):
    def __init__(self, on_change=None):
        super().__init__(
            bgcolor=colors.GREY_100,
            border_radius=12,
            border_width=1,
            border_color=colors.GREY_100,
            focused_border_color=colors.BLUE,
            filled=True,
            height=44,
            text_style=TextStyle(
                size=12,
                color=colors.BLACK,
            ),
            on_change=on_change,
        )