from windows_use.agent.registry.views import ToolResult
from windows_use.agent.desktop.service import Desktop
from windows_use.agent.tools import Tool

class Registry:
    def __init__(self,tools:list[Tool]=[]):
        self.tools=tools
        self.tools_registry=self.registry()

    def registry(self)->dict[str,Tool]:
        return {tool.name: tool for tool in self.tools}
    
    def get_tools(self,exclude_tools:list[str]=[])->list[Tool]:
        if not exclude_tools:
            return self.tools
        return [tool for tool in self.tools if tool.name not in exclude_tools]

    def get_tool(self,tool_name:str)->Tool|None:
        return self.tools_registry.get(tool_name,None)
    
    def get_tools_schema(self) -> list[dict]:
        tools = [tool.json_schema for tool in self.tools]
        return tools
    
    def execute(self, tool_name: str, tool_params: dict, desktop: Desktop|None=None) -> ToolResult:
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult(is_success=False, error=f"Tool '{tool_name}' not found.")
        errors=tool.validate_params(tool_params)
        if errors:
            error_msg="\n".join(errors)
            return ToolResult(is_success=False, error=f"Tool '{tool_name}' validation failed:\n{error_msg}")
        try:
            content = tool.invoke(**({'desktop': desktop} | tool_params))
            return ToolResult(is_success=True, content=content)
        except Exception as error:
            error_msg=str(error)
            return ToolResult(is_success=False, error=f"Tool '{tool_name}' execution failed:\n{error_msg}")

    async def aexecute(self, tool_name: str, tool_params: dict, desktop: Desktop|None=None) -> ToolResult:
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult(is_success=False, error=f"Tool '{tool_name}' not found.")
        errors = tool.validate_params(tool_params)
        if errors:
            error_msg = "\n".join(errors)
            return ToolResult(is_success=False, error=f"Tool '{tool_name}' validation failed:\n{error_msg}")
        try:
            content = await tool.ainvoke(**({'desktop': desktop} | tool_params))
            return ToolResult(is_success=True, content=content)
        except Exception as error:
            error_msg = str(error)
            return ToolResult(is_success=False, error=f"Tool '{tool_name}' async execution failed:\n{error_msg}")
