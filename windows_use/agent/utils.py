from windows_use.llms.base import ChatLLMResponse
from windows_use.agent.views import AgentData
from windows_use.messages import AIMessage
import json
import ast
import re

def xml_parser(message: ChatLLMResponse) -> AgentData:
    if isinstance(message.content, AIMessage):
        text = message.content.content
    else:
        text = str(message.content)

    # Dictionary to store extracted values
    result = {}
    # Extract Evaluate
    evaluate_match = re.search(r"<evaluate>(.*?)<\/evaluate>", text, re.DOTALL)
    if evaluate_match:
        result['evaluate'] = evaluate_match.group(1).strip()
    # Extract Thought
    thought_match = re.search(r"<thought>(.*?)<\/thought>", text, re.DOTALL)
    if thought_match:
        result['thought'] = thought_match.group(1).strip()
    # Extract Action
    action_name_match = re.search(r"<name>(.*?)<\/name>", text, re.DOTALL)
    if action_name_match:
        action = {}
        action['name'] = action_name_match.group(1).strip()

        # Extract and convert Action-Input to a dictionary
        action_input_match = re.search(r"<input>(.*?)<\/input>", text, re.DOTALL)
        if action_input_match:
            action_input_str = action_input_match.group(1).strip()
            try:
                # First try to evaluate as a Python literal (handles Python dicts)
                action['params'] = ast.literal_eval(action_input_str)
            except (ValueError, SyntaxError):
                try:
                    # Fallback to JSON parsing
                    action['params'] = json.loads(action_input_str)
                except json.JSONDecodeError:
                    # If both fail, we can't parse params as a dict.
                    # Depending on strictness, we might want to error or leave params empty.
                    # Here we will raise to inform the caller/system of invalid format.
                    raise ValueError(f"Failed to parse action params: {action_input_str}")

        result['action'] = action

    try:
        return AgentData.model_validate(result)
    except Exception as e:
        raise ValueError(f"Validation failed: {e}")

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()
