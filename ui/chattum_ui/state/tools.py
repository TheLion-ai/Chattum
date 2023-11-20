from .state import State
import reflex as rx
from typing import Optional
from chattum_ui.utils import backend_controller as bc


class UserVariable(rx.Base):
    name: str = rx.Var[str]
    description: str = rx.Var[str]
    value: Optional[str] = rx.Var[str]
    form_type: str = rx.Var[str]


class ToolsState(State):
    tools: list[dict] = []
    _tools_dict: dict = {}

    available_tools = []
    new_tool_name: str = None

    creating_new_tool: bool = False
    variables_changed: bool = False

    tool_id: str = None
    tool: dict = {}
    _user_variables: list[UserVariable] = []

    def load_tools(self) -> None:
        self.tools = bc.get_tools(self.bot_id)
        self._tools_dict = (
            {tool["id"]: tool for tool in self.tools} if self.tools else {}
        )
        self.available_tools = bc.get_available_tools(self.bot_id)
        print(self.tools)

    @rx.var
    def available_tools_names(self) -> list[str]:
        return [tool["name"] for tool in self.available_tools]

    @rx.var
    def new_tool_description(self) -> str:
        for tool in self.available_tools:
            if tool["name"] == self.new_tool_name:
                return tool["user_description"]
        return ""

    def load_tool(self, tool_id: str) -> None:
        self._user_variables = []
        self.tool = {}
        self.tool_id = tool_id
        self.tool = self._tools_dict[tool_id]
        self.load_user_variables()
        self.variables_changed = False

    def load_user_variables(self) -> list[UserVariable]:
        self._user_variables = [
            UserVariable(
                name=variable["name"],
                description=variable["description"],
                value=variable["value"],
                form_type=variable["form_type"],
            )
            for variable in self.tool.get("user_variables", [])
        ]
        print(self._user_variables)

    @rx.var
    def user_variables(self) -> list[UserVariable]:
        print("get user variables")
        print(self._user_variables)
        return self._user_variables

    def update_user_variable(self, variable_name, variable_value) -> None:
        for variable in self._user_variables:
            if variable.name == variable_name:
                variable.value = variable_value
                break
        self.variables_changed = True

    def get_user_variable_value(self, variable_name) -> str:
        for variable in self._user_variables:
            if variable.name == variable_name:
                return variable.value

        print(self.user_variables)

    def create_new_tool(self) -> None:
        self.tool_id = None
        for tool in self.available_tools:
            if tool["name"] == self.new_tool_name:
                self.tool = tool
                break
        self.load_user_variables()

    def update_tool(self) -> None:
        user_variables = [
            {
                "name": variable.name,
                "description": variable.description,
                "value": variable.value,
                "form_type": variable.form_type,
            }
            for variable in self._user_variables
        ]
        bc.create_new_tool(self.bot_id, self.new_tool_name, user_variables)
        self.load_tools()
        self.creating_new_tool = False
        # print(self._user_variables)
        # print(self)

    def delete_tool(self) -> None:
        bc.delete_tool(self.bot_id, self.tool_id)
        self.load_tools()
        self.tool_id = None
        self.tool = {}

    def toggle_creating_new_tool(self) -> None:
        if self.creating_new_tool:
            self.creating_new_tool = False
            self.new_tool_name = None
            self.tool = {}
            self.tool_id = None
        else:
            self.creating_new_tool = True
            self.new_tool_name = None
            self.tool = {}
            self.tool_id = None

    def set_new_tool_name(self, new_tool_name: str) -> None:
        self.new_tool_name = new_tool_name
        self.tool_id = None
        for tool in self.available_tools:
            if tool["name"] == self.new_tool_name:
                self.tool = tool
                break
        self.load_user_variables()
