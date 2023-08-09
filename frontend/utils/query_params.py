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
        if param in st.experimental_get_query_params():
            value = st.experimental_get_query_params()[param][0]
            value = None if value == "None" else value
        else:
            value = None
        return value

    def set_to_url(self, **kwargs: dict) -> None:
        """Set the value of a parameter in the URL."""
        current_query_params = st.experimental_get_query_params()
        query_params = {**current_query_params, **kwargs}
        st.experimental_set_query_params(**query_params)

    def __post_init__(self) -> None:
        """Load the values from the URL on init."""
        for field in fields(self):
            setattr(self, field.name, self.get_form_url(field.name))
