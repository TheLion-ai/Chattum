import streamlit as st
from backend_controller import (
    create_new_tool,
    delete_tool,
    get_available_tools,
    get_tools,
)
from streamlit_ace import st_ace
from utils import query_params


class ToolsPanel:
    def __init__(self, bot_id):
        self.bot_id = bot_id
        self.available_tools = get_available_tools(self.bot_id)
        self.available_tools_dict = {
            tool["name"]: tool for tool in self.available_tools
        }

        self.tools = get_tools(self.bot_id)
        self.tools_dict = {tool["id"]: tool for tool in self.tools}

        self._selected_tool_id = query_params.get_form_url("tool_id")
        self._selected_tool = self.tools_dict.get(self._selected_tool_id, None)

    def __call__(self):
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

    def _display_new_tool(self):
        new_tool_name = st.selectbox("Select tool", self.available_tools_dict.keys())
        new_tool = self.available_tools_dict[new_tool_name]
        self._display_tool_form(new_tool)

    def _display_tool_form(self, tool, key="tool_form"):
        tool_variables = tool["user_variables"]
        st.write(tool["user_description"])
        with st.form(key=key):
            for user_variable in tool_variables:

                if user_variable["form_type"] == "text":
                    user_variable["value"] = st.text_input(
                        user_variable["name"], value=user_variable.get("value", "")
                    )
                elif user_variable["form_type"] == "editor":
                    st.write(user_variable["name"])
                    user_variable["value"] = st_ace(
                        language="handlebars", value=user_variable.get("value", "")
                    )
            col1, _, col2 = st.columns([2, 3, 2])
            with col1:
                submit_button = st.form_submit_button(
                    "Update tool", type="primary", use_container_width=True
                )
                if submit_button:
                    create_new_tool(self.bot_id, tool["name"], tool_variables)
                    st.rerun()
            with col2:
                delete_button = st.form_submit_button(
                    "🗑️Delete tool", type="secondary", use_container_width=True
                )
                if delete_button:
                    delete_tool(self.bot_id, tool["id"])
                    st.rerun()
