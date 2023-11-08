"""Gather all tools in one place."""
from .requests_tools import PostTool
from .sms_tools import TwilloTool

available_tools = [PostTool, TwilloTool]
available_tools_dict = {tool.name: tool for tool in available_tools}  # type: ignore
