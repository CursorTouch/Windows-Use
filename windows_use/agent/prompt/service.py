from windows_use.agent.desktop.views import DesktopState, Browser
from windows_use.agent.views import AgentData,AgentStep
from windows_use.agent.registry.views import ToolResult
from windows_use.agent.desktop.service import Desktop
from importlib.resources import files
from datetime import datetime
from getpass import getuser
from pathlib import Path
import pyautogui as pg

class Prompt:
    @staticmethod
    def system_prompt(desktop:Desktop,browser: Browser,language: str,tools_prompt:str,max_steps:int,instructions: list[str]=[]) -> str:
        width, height = pg.size()
        template =Path(files('windows_use.agent.prompt').joinpath('system.md')).read_text()
        return template.format(**{
            'datetime': datetime.now().strftime('%A, %B %d, %Y'),
            'instructions': '\n'.join(instructions),
            'tools_prompt': tools_prompt,
            'download_directory': Path.home().joinpath('Downloads').as_posix(),
            'os':desktop.get_windows_version(),
            'language':language,
            'browser':browser.value,
            'home_dir':Path.home().as_posix(),
            'user':f"{getuser()} ({desktop.get_user_account_type()})",
            'resolution':f'Primary Monitor ({width}x{height}) with DPI Scale: {desktop.get_dpi_scaling()}',
            'max_steps': max_steps
        })
    
    @staticmethod
    def action_prompt(agent_data:AgentData) -> str:
        template = Path(files('windows_use.agent.prompt').joinpath('action.md')).read_text()
        return template.format(**{
            'evaluate': agent_data.evaluate,
            'thought': agent_data.thought,
            'action_name': agent_data.action.name,
            'action_input': agent_data.action.params
        })
    
    @staticmethod
    def previous_observation_prompt(agent_step:AgentStep,observation: str)-> str:
        template=Path(files('windows_use.agent.prompt').joinpath('previous_observation.md')).read_text()
        steps = agent_step.steps
        max_steps = agent_step.max_steps
        return template.format(**{
            'steps': steps,
            'max_steps': max_steps,
            'observation': observation
        })
         
    @staticmethod
    def observation_prompt(query:str,agent_step:AgentStep, tool_result:ToolResult,desktop_state: DesktopState) -> str:
        cursor_location = pg.position()
        tree_state = desktop_state.tree_state
        steps = agent_step.steps
        max_steps = agent_step.max_steps
        template = Path(files('windows_use.agent.prompt').joinpath('observation.md')).read_text()
        return template.format(**{
            'steps': steps,
            'max_steps': max_steps,
            'observation': tool_result.content if tool_result.is_success else tool_result.error,
            'active_app': desktop_state.active_app_to_string(),
            'cursor_location': f'({cursor_location.x},{cursor_location.y})',
            'apps': desktop_state.apps_to_string(),
            'interactive_elements': tree_state.interactive_elements_to_string() or 'No interactive elements found',
            'scrollable_elements': tree_state.scrollable_elements_to_string() or 'No scrollable elements found',
            'query':query
        })
    
    @staticmethod
    def answer_prompt(agent_data: AgentData, tool_result: ToolResult):
        template = Path(files('windows_use.agent.prompt').joinpath('answer.md')).read_text()
        return template.format(**{
            'evaluate': agent_data.evaluate,
            'thought': agent_data.thought,
            'final_answer': tool_result.content
        })

    
