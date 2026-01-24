from windows_use.llms.base import ChatLLMResponse
from windows_use.agent.views import AgentData, Action
from windows_use.messages import AIMessage
import json
import re

def json_parser(message: ChatLLMResponse) -> AgentData:
    """
    Parse LLM response content into AgentData object.
    Handles JSON with or without markdown code blocks.
    
    Args:
        message: ChatLLMResponse object containing the raw text from LLM
        
    Returns:
        AgentData object
        
    Raises:
        ValueError: If JSON is invalid or missing required fields
    """
    if isinstance(message.content, AIMessage):
        content = message.content.content
    else:
        content = str(message.content)

    # Extract JSON if it's wrapped in markdown code blocks
    if "```json" in content:
        json_start = content.find("```json") + 7
        json_end = content.find("```", json_start)
        content = content[json_start:json_end].strip()
    elif "```" in content:
        json_start = content.find("```") + 3
        json_end = content.find("```", json_start)
        content = content[json_start:json_end].strip()
    
    # Clean up the text to find JSON content if no code blocks
    content = content.strip()
    
    # Fallback: Try to find the first opening brace and last closing brace if parsing fails or no blocks
    if not (content.startswith('{') and content.endswith('}')):
        start = content.find('{')
        end = content.rfind('}')
        if start != -1 and end != -1:
            content = content[start:end+1]

    # Parse JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}\nContent: {content}")
    
    # Validate required fields
    required_fields = ["thought", "evaluate", "action"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {missing_fields}")
    
    # Validate action structure
    if not isinstance(data["action"], dict):
        raise ValueError("'action' must be a dictionary")
    
    if "name" not in data["action"]:
        raise ValueError("'action' must contain 'name'")
    
    if "params" not in data["action"]:
        # Allow missing params, default to empty dict
        data["action"]["params"] = {}
    
    # Create AgentData
    return AgentData(
        thought=data["thought"],
        evaluate=data["evaluate"],
        action=Action(
            name=data["action"]["name"],
            params=data["action"]["params"]
        )
    )

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()
