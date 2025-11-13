from windows_use.agent.registry.views import ToolResult
from windows_use.agent.desktop.service import Desktop
from windows_use.tool import Tool
from textwrap import dedent
import json

class Registry:
    def __init__(self,tools:list[Tool]=[]):
        self.tools=tools
        self.tools_registry=self.registry()

    def tool_prompt(self, tool_name: str) -> str:
        tool = self.tools_registry.get(tool_name)
        if tool is None:
            return f"Tool '{tool_name}' not found."
        return dedent(f"""
        Tool Name: {tool.name}
        Tool Description: {tool.description}
        Tool Schema: {json.dumps(tool.args_schema,indent=4)}
        """)

    def registry(self):
        return {tool.name: tool for tool in self.tools}
    
    def get_tools_prompt(self) -> str:
        tools_prompt = [self.tool_prompt(tool.name) for tool in self.tools]
        return '\n\n'.join(tools_prompt)
    
    def execute(self, tool_name: str, desktop: Desktop|None=None, **kwargs) -> ToolResult:
        tool = self.tools_registry.get(tool_name)
        if tool is None:
            return ToolResult(is_success=False, error=f"Tool '{tool_name}' not found.")
        try:
            args=tool.model.model_validate(kwargs)
            content = tool.invoke(**({'desktop': desktop} | args.model_dump()))
            return ToolResult(is_success=True, content=content)
        except Exception as error:
            return ToolResult(is_success=False, error=str(error))