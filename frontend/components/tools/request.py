"""Requests tool component. Used to make requests to a given URL and communicate with external APIs."""
from dataclasses import dataclass, field
from typing import Literal

import streamlit as st


@dataclass
class RequestsTool:
    """Requests tool component. Used to make requests to a given URL and communicate with external APIs."""

    url: str = ""
    schema: Literal["GET", "POST", "PUT", "DELETE"] = "GET"
    description: str = field(default_factory=str)
    parameters: list[dict] = field(default_factory=list)
    body: dict = field(default_factory=dict)

    def render(self) -> None:
        """Render the streamlit components."""
        st.title("Requests Tool")

        self.url = st.text_input("URL", self.url)
        self.schema = st.selectbox("Schema", self.schema)
        for i, parameter in enumerate(self.parameters):
            self.parameters[i]["name"] = st.text_input("Name", parameter["name"])
            self.parameters[i]["description"] = st.text_input(
                "Description", parameter["description"]
            )
