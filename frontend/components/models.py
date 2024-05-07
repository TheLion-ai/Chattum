from typing import Any

import streamlit as st
from backend_controller import change_model, get_available_models, get_bot, get_model


class ModelPanel:
    def __init__(self, bot_id: str) -> None:
        self.bot_id = bot_id

        self.model = get_model(self.bot_id)

        self.available_models = get_available_models(self.bot_id)
        self.available_models_dict = {
            model["name"]: model for model in self.available_models
        }

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.model is not None:
            index = (
                list(self.available_models_dict.keys()).index(self.model["name"])
                if self.model["name"] in self.available_models_dict.keys()
                else 0
            )
        else:
            index = 0
        self._selected_model_name = st.selectbox(
            "Select model", self.available_models_dict.keys(), index=index
        )
        if self._selected_model_name is not None:
            if (
                self.model is not None
                and self._selected_model_name == self.model["name"]
            ):
                self._selected_model = self.model
            else:
                self._selected_model = self.available_models_dict[
                    self._selected_model_name
                ]
            # st.write(self._selected_model)
            self._display_model_form(self._selected_model)

    def _display_model_form(self, model: dict, key: str = "model_form") -> None:
        model_variables = model["user_variables"]
        st.write(model["user_description"])
        # st.write(model_variables)
        with st.form(key=key):
            for user_variable in model_variables:

                st.write(user_variable["name"])
                st.write(user_variable["description"])
                if user_variable["available_values"] is not None:
                    value = (
                        user_variable.get("value")
                        or user_variable.get("default_value")
                        or ""
                    )
                    index = (
                        user_variable["available_values"].index(value)
                        if value in user_variable["available_values"]
                        else 0
                    )
                    user_variable["value"] = st.selectbox(
                        user_variable["name"],
                        user_variable["available_values"],
                        index=index,
                        label_visibility="collapsed",
                    )

                elif user_variable["form_type"] == "text":
                    value = (
                        user_variable.get("value")
                        or user_variable.get("default_value")
                        or ""
                    )
                    user_variable["value"] = st.text_input(
                        user_variable["name"], value=value, label_visibility="collapsed"
                    )
                elif user_variable["form_type"] == "secret":
                    st.write("Secret")
                    value = (
                        user_variable.get("value")
                        or user_variable.get("default_value")
                        or ""
                    )
                    user_variable["value"] = st.text_input(
                        user_variable["name"],
                        value=value,
                        label_visibility="collapsed",
                        type="password",
                    )
                elif user_variable["form_type"] == "float":
                    value = user_variable.get("value")
                    if value is None:
                        value = user_variable.get("default_value")
                    user_variable["value"] = st.number_input(
                        user_variable["name"], value=value, label_visibility="collapsed"
                    )

            col1, _, col2 = st.columns([2, 3, 2])
            with col1:
                submit_button = st.form_submit_button(
                    "Update model", type="primary", use_container_width=True
                )
                if submit_button:
                    change_model(self.bot_id, model)
                    pass
