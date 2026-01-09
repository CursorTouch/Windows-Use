from windows_use.agent.registry.views import ToolResult
from windows_use.agent.desktop.service import Desktop
from windows_use.tool import Tool
from windows_use.tool.service import ToolResult as RawToolResult
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
            # Preprocess common alternative selectors (e.g., label -> loc)
            if desktop and 'label' in kwargs and 'loc' not in kwargs:
                try:
                    label = int(kwargs.pop('label'))
                    coords = desktop.get_coordinates_from_label(label)
                    kwargs['loc'] = coords
                except (IndexError, ValueError) as e:
                    return ToolResult(is_success=False, error=f"Invalid label selector: {e}")

            args=tool.model.model_validate(kwargs)
            raw = tool.invoke(**({'desktop': desktop} | args.model_dump()))
            # If tool returned a Raw ToolResult (from windows_use.tool.service), map it
            if isinstance(raw, RawToolResult):
                is_ok = raw.status.lower() in ("ok", "success")
                content_str = None
                if raw.evidence:
                    # Prefer a readable representation of evidence
                    try:
                        import json
                        content_str = json.dumps(raw.evidence)
                    except Exception:
                        content_str = str(raw.evidence)
                elif raw.details:
                    content_str = str(raw.details)
                else:
                    content_str = None
                return ToolResult(is_success=is_ok, content=content_str, error=None if is_ok else str(raw.details), confidence=raw.confidence, evidence=raw.evidence)
            # If tool returned arbitrary dict or string, normalize
            if isinstance(raw, dict):
                return ToolResult(is_success=True, content=str(raw))
            if isinstance(raw, str):
                return ToolResult(is_success=True, content=raw)
            return ToolResult(is_success=True, content=str(raw))
        except Exception as error:
            return ToolResult(is_success=False, error=str(error))