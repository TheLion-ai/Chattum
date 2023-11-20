"""Welcome to Reflex!."""
import reflex as rx
from chattum_ui import styles

# Import all the pages.
from chattum_ui.pages import *
from pydantic import BaseModel

# Create the app and compile it.
app = rx.App(style=styles.base_style)


class TestModel(BaseModel):
    message: str


def api_test(item_id: str, response_model: TestModel):
    return {"message": "Hello World!"}


app.api.add_api_route("/items/{item_id}", api_test)
app.compile()
