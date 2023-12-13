from flet import *

class TextButtonChattum(UserControl):
    def __init__(self, text, on_click):
        super().__init__()
        self.text_button = TextButton(
            content=Text(
                text,
                style=TextThemeStyle.BODY_SMALL, 
                color=colors.BLACK,
            ),
            style=ButtonStyle(
                animation_duration=200,
                color={
                    MaterialState.HOVERED: colors.BLUE,
                    MaterialState.FOCUSED: colors.WHITE,
                    MaterialState.PRESSED: colors.WHITE,
                    MaterialState.DEFAULT: colors.BLACK,
                },
                bgcolor={
                    MaterialState.HOVERED: colors.WHITE, 
                    MaterialState.FOCUSED: colors.BLUE, 
                    MaterialState.PRESSED: colors.WHITE,
                    MaterialState.DEFAULT: colors.WHITE,
                },
                overlay_color={
                    MaterialState.PRESSED: colors.with_opacity(0.8, colors.BLUE),
                },
                # shadow_color={
                #     MaterialState.DEFAULT: colors.RED,   
                # },
                elevation={
                    MaterialState.PRESSED: 0, 
                    MaterialState.DEFAULT: 1,
                },
                side={
                    MaterialState.HOVERED: BorderSide(1, colors.BLUE),
                    MaterialState.FOCUSED: BorderSide(1, colors.BLUE),
                    MaterialState.DEFAULT: BorderSide(1, colors.BLACK12), 
                },
                shape={
                    MaterialState.DEFAULT: RoundedRectangleBorder(radius=10), 
                },
            ),
            on_click=on_click
        )

    def build(self):
        return self.text_button