from windows_use.agent.registry.views import ToolResult
from windows_use.agent.desktop.service import Desktop
from windows_use.tool import Tool

class Registry:
    def __init__(self,tools:list[Tool]=[]):
        self.tools=tools
        self.tools_registry=self.registry()

    def registry(self)->dict[str,Tool]:
        return {tool.name: tool for tool in self.tools}
    
    def get_tools(self)->list[Tool]:
        return self.tools

    def get_tool(self,tool_name:str)->Tool|None:
        return self.tools_registry.get(tool_name,None)
    
    def get_tools_schema(self) -> list[dict]:
        tools = [tool.json_schema for tool in self.tools]
        return tools
    
    def execute(self, tool_name: str, desktop: Desktop|None=None, **kwargs) -> ToolResult:
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult(is_success=False, error=f"Tool '{tool_name}' not found.")
        errors=tool.validate(kwargs)
        if errors:
            error_msg="\n".join(errors)
            return ToolResult(is_success=False, error=f"Tool '{tool_name}' validation failed:\n{error_msg}")
        try:
            content = tool.invoke(**({'desktop': desktop} | kwargs))
            return ToolResult(is_success=True, content=content)
        except Exception as error:
            error_msg=str(error)
            return ToolResult(is_success=False, error=f"Tool '{tool_name}' execution failed:\n{error_msg}")