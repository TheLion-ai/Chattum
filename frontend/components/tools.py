"""Compontents for tools."""

import streamlit as st
from backend_controller import (
    create_or_edit_tool,
    delete_tool,
    get_available_tools,
    get_tools,
)
from streamlit_ace import st_ace
from utils import query_params


class ToolsPanel:
    """Tools panel."""

    def __init__(self, bot_id: str) -> None:
        """Initialize the tools panel, load tools using the bot id."""
        self.bot_id = bot_id
        self.available_tools = get_available_tools(self.bot_id)
        self.available_tools_dict = {
            tool["name"]: tool for tool in self.available_tools
        }
        # st.write(self.available_tools)

        self.tools = get_tools(self.bot_id)
        self.tools_dict = {tool["id"]: tool for tool in self.tools}

        self._selected_tool_id = query_params.get_from_url_or_state("tool_id")
        self._selected_tool = self.tools_dict.get(self._selected_tool_id, None)

    def __call__(self) -> None:
        """Display the tools panel."""
        with st.expander("Add new tool"):
            self._display_new_tool()

        st.divider()
        tools_list, tool_content = st.columns([3, 5], gap="large")

        with tools_list:
            for tool in self.tools:
                st.button(
                    tool["name"],
                    use_container_width=True,
                    on_click=query_params.set_to_url,
                    kwargs={"tool_id": tool["id"]},
                    type="primary" if self._selected_tool == tool else "secondary",
                    key=f"tool_{tool['id']}",
                )
        with tool_content:
            if self._selected_tool is not None:
                self._display_tool_form(
                    self._selected_tool, key=f"{self._selected_tool['id']}_form"
                )

    def _display_new_tool(self) -> None:
        """Display the new tool form."""
        new_tool_name = st.selectbox("Select tool", self.available_tools_dict.keys())
        new_tool = self.available_tools_dict[new_tool_name]
        self._display_tool_form(new_tool)

    def _display_tool_form(self, tool: dict, key: str = "tool_form") -> None:
        """Display the tool form."""
        tool_variables = tool["user_variables"]
        name_for_bot = st.text_input(
            "Name of the tool for the bot",
            value=tool.get("name_for_bot", ""),
            key=f"{tool['id']}_name_for_bot",
        )

        bot_description = st.text_input(
            "Description of the tool for the bot",
            value=tool.get("description_for_bot", ""),
            key=f"{tool['id']}_bot_description",
        )
        with st.form(key=key):
            for user_variable in tool_variables:

                if user_variable["form_type"] == "text":
                    user_variable["value"] = st.text_input(
                        user_variable["name"], value=user_variable.get("value", "")
                    )
                elif user_variable["form_type"] == "editor":
                    st.write(user_variable["name"])
                    user_variable["value"] = st_ace(
                        language="handlebars",
                        value=user_variable.get("value", ""),
                        theme="twilight",
                    )
            col1, _, col2 = st.columns([2, 3, 2])
            with col1:
                submit_button = st.form_submit_button(
                    "Update tool", type="primary", use_container_width=True
                )
                if submit_button:
                    st.write("submit")
                    create_or_edit_tool(
                        self.bot_id,
                        tool["name"],
                        bot_description,
                        tool_variables,
                        tool["id"],
                        name_for_bot=name_for_bot,
                    )
                    st.rerun()
            with col2:
                delete_button = st.form_submit_button(
                    "🗑️Delete tool", type="secondary", use_container_width=True
                )
                if delete_button:
                    delete_tool(self.bot_id, tool["id"])
                    st.rerun()
