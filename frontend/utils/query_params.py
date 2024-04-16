"""Loading and storing variables in the URL query parameters.""" ""
from dataclasses import dataclass, fields

import streamlit as st


@dataclass
class QueryParams:
    """Loading and storing variables in the URL query parameters."""

    page: str | None = None
    bot_id: str | None = None
    conversation_id: str | None = None

    def get_form_url(self, param: str) -> str:
        """Get the value of a parameter from the URL."""
        if param in st.query_params:
            value = st.query_params[param][0]
            value = None if value == "None" else value
        else:
            value = None
        return value

    def get_from_url_or_state(self, param: str) -> str:
        """Get the value of a parameter from the URL or the state."""
        if param in st.query_params:
            value = st.query_params[param]
        elif param in st.session_state:
            value = st.session_state[param]
            self.set_to_url(**{param: value})
        else:
            value = None
        return value

    def set_to_url(self, **kwargs: dict) -> None:
        """Set the value of a parameter in the URL."""
        for key, value in kwargs.items():
            st.query_params[key] = value

    def set_to_url_and_state(self, **kwargs: dict) -> None:
        """Set the value of a parameter in the URL and the state."""
        for key, value in kwargs.items():
            st.query_params[key] = value
            st.session_state[key] = value

    def __post_init__(self) -> None:
        """Load the values from the URL on init."""
        for field in fields(self):
            setattr(self, field.name, self.get_form_url(field.name))
