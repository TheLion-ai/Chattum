from dataclasses import dataclass, field

import streamlit as st


@dataclass
class RequestsTool:
    url: str = None
    schema: str = field(default_factory=lambda: ["GET", "POST", "PUT", "DELETE"])
    description: str = field(default_factory=str)
    parameters: list[dict] = field(default_factory=list)
    body: dict = field(default_factory=dict)

    def render(self) -> None:
        st.title("Requests Tool")

        self.url = st.text_input("URL", self.url)
        self.schema = st.selectbox("Schema", self.schema)
        for parameter in enumerate(self.parameters):
            self.parameter["name"] = st.text_input("Name", parameter["name"])
            self.parameter["description"] = st.text_input(
                "Description", parameter["description"]
            )
