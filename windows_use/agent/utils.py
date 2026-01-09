import re
import ast
import json

#
from typing import Any, TypeVar, Type
from pydantic import BaseModel

#
from windows_use.llms.base import BaseChatLLM
from windows_use.messages import BaseMessage
from windows_use.llms.views import ChatLLMResponse
from windows_use.agent.views import AgentData


T = TypeVar('T', bound=BaseModel)

class RobustJSONDecoder:
    """
    ## Robust JSON decoder with support for:
    - Comments (// and /* */)
    - Trailing commas
    - Single quotes
    - Unquoted keys
    """

    @classmethod
    def decode(cls, text: str) -> Any:
        """Decode 'dirty' JSON"""
        cleaned = text

        # Remove multiline comments /* */
        cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)

        # Remove single-line comments //
        cleaned = re.sub(r'//[^\n]*', '', cleaned)

        # Trailing commas
        cleaned = re.sub(r',(\s*[}\]])', r'\1', cleaned)

        # Attempt 1: standard JSON
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # Attempt 2: replace single quotes with double
        try:
            # Careful with quotes inside strings
            fixed_quotes = cls._fix_quotes(cleaned)
            return json.loads(fixed_quotes)
        except json.JSONDecodeError:
            pass

        # Attempt 3: ast.literal_eval (Python syntax)
        try:
            return ast.literal_eval(cleaned)
        except (ValueError, SyntaxError):
            pass

        raise ValueError(f"Cannot decode JSON: {text[:100]}...")

    @staticmethod
    def _fix_quotes(text: str) -> str:
        """Replace single quotes with double quotes (carefully)"""
        result = []
        in_double = False
        in_single = False
        prev_char = ''

        for char in text:
            if char == '"' and prev_char != '\\' and not in_single:
                in_double = not in_double
                result.append(char)
            elif char == "'" and prev_char != '\\' and not in_double:
                in_single = not in_single
                result.append('"')  # Replace with double quote
            else:
                result.append(char)
            prev_char = char

        return ''.join(result)


class ContentExtractor:
    """Utilities for extracting data from LLM responses with garbage"""

    # Patterns for cleaning JSON
    JSON_CLEANUP_PATTERNS = [
        # Markdown code blocks
        (r"```json\s*\n?", ""),
        ## (r"```\s*\n?", ""),
        # Single-line comments (// ...)
        (r"//[^\n]*\n?", "\n"),
        # Trailing commas before closing brackets
        (r",(\s*[}\]])", r"\1"),
        # BOM and invisible characters
        (r"^\ufeff", ""),
        (r"[\x00-\x08\x0b\x0c\x0e-\x1f]", ""),
    ]

    @classmethod
    def extract_json(cls, text: str, strict: bool = False) -> dict | list | None:
        """
        Extract JSON from text with garbage.

        Tries several strategies:
        1. Direct parsing (if text is clean)
        2. Extraction from markdown code block
        3. Search for first valid JSON object/array
        4. Cleanup and re-parsing
        """
        if not text:
            return None

        text = text.strip()

        # Strategy 1: Direct parsing
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Strategy 2: Extraction from code block
        code_block_match = re.search(
            r"```(?:json)?\s*\n?(.*?)\n?```",
            text,
            re.DOTALL | re.IGNORECASE
        )
        if code_block_match:
            try:
                return json.loads(code_block_match.group(1).strip())
            except json.JSONDecodeError:
                pass

        # Strategy 3: Find first JSON object {...} or array [...]
        json_obj = cls._find_json_object(text)
        if json_obj is not None:
            return json_obj

        # Strategy 4: Cleanup from comments and garbage
        cleaned = cls._cleanup_json_string(text)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # Strategy 5: Search JSON after cleanup
        json_obj = cls._find_json_object(cleaned)
        if json_obj is not None:
            return json_obj

        if strict:
            raise ValueError(f"Could not extract valid JSON from text: {text[:200]}...")

        return None

    @classmethod
    def _find_json_object(cls, text: str) -> dict | list | None:
        """Find and extract first valid JSON object or array"""
        # Looking for JSON start
        for i, char in enumerate(text):
            if char == '{':
                result = cls._try_parse_from_position(text, i, '{', '}')
                if result is not None:
                    return result
            elif char == '[':
                result = cls._try_parse_from_position(text, i, '[', ']')
                if result is not None:
                    return result
        return None

    @classmethod
    def _try_parse_from_position(
        cls,
        text: str,
        start: int,
        open_char: str,
        close_char: str
    ) -> dict | list | None:
        """Try to parse JSON starting from position"""
        depth = 0
        in_string = False
        escape_next = False

        for i in range(start, len(text)):
            char = text[i]

            if escape_next:
                escape_next = False
                continue

            if char == '\\' and in_string:
                escape_next = True
                continue

            if char == '"' and not escape_next:
                in_string = not in_string
                continue

            if in_string:
                continue

            if char == open_char:
                depth += 1
            elif char == close_char:
                depth -= 1
                if depth == 0:
                    candidate = text[start:i+1]
                    try:
                        return json.loads(candidate)
                    except json.JSONDecodeError:
                        # Let's try to clean and parse again
                        cleaned = cls._cleanup_json_string(candidate)
                        try:
                            return json.loads(cleaned)
                        except json.JSONDecodeError:
                            return None
        return None

    @classmethod
    def _cleanup_json_string(cls, text: str) -> str:
        """Clean JSON string from comments and garbage"""
        result = text
        for pattern, replacement in cls.JSON_CLEANUP_PATTERNS:
            result = re.sub(pattern, replacement, result)
        return result.strip()

    @classmethod
    def extract_xml_tag(
        cls,
        text: str,
        tag: str,
        default: str | None = None
    ) -> str | None:
        """Extract XML tag content"""
        pattern = rf"<{tag}>(.*?)</{tag}>"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return default

    @classmethod
    def extract_xml_tag_as_json(
        cls,
        text: str,
        tag: str
    ) -> dict | list | None:
        """Extract XML tag content and parse as JSON"""
        content = cls.extract_xml_tag(text, tag)
        if content:
            return cls.extract_json(content)
        return None

    @classmethod
    def extract_all_xml_tags(cls, text: str) -> dict[str, str]:
        """Extract all XML tags from text"""
        pattern = r"<(\w+)>(.*?)</\1>"
        matches = re.findall(pattern, text, re.DOTALL)
        return {tag: content.strip() for tag, content in matches}

def get_agent_action(llm: BaseChatLLM, messages: list[BaseMessage]) -> AgentData:
    """Get agent action with fallback to parsing"""
    try:
        # Preferably: structured output
        return extract_agent_data_structured(llm, messages)
    except Exception as e:
        print(f"[Agent] Error extracting agent action: {e}")
        # Fallback: parsing from text
        response = llm.invoke(messages)
        return extract_agent_data(response)

def extract_agent_data(message: ChatLLMResponse) -> AgentData:
    """
    Extract agent data from LLM response.
    Handles various formats and garbage in the response.
    """
    text = message.content

    if not text:
        raise ValueError("Empty message content")

    result = {}
    extractor = ContentExtractor

    # === Strategy 1: Clean JSON (structured output) ===
    # If the model returned clean JSON without tags
    if text.strip().startswith('{') or text.strip().startswith('```'):
        json_data = extractor.extract_json(text)
        if json_data and isinstance(json_data, dict):
            # Check if this looks like our format
            if 'action' in json_data or 'thought' in json_data:
                try:
                    return AgentData.model_validate(json_data)
                except Exception:
                    pass  # Continue with XML parsing

    # === Strategy 2: XML tags ===
    # Extract Evaluate
    evaluate = extractor.extract_xml_tag(text, "evaluate")
    if evaluate:
        result['evaluate'] = evaluate

    # Extract Thought
    thought = extractor.extract_xml_tag(text, "thought")
    if thought:
        result['thought'] = thought

    # Extract Action
    action = {}

    # Action Name
    action_name = extractor.extract_xml_tag(text, "action_name")
    if action_name:
        action['name'] = action_name

    # Action Input (can be JSON or dict-like string)
    action_input_raw = extractor.extract_xml_tag(text, "action_input")
    if action_input_raw:
        action['params'] = _parse_action_params(action_input_raw)

    if action:
        result['action'] = action

    # === Strategy 3: Search JSON inside text ===
    if not result.get('action'):
        # JSON might be somewhere in the text
        json_data = extractor.extract_json(text)
        if json_data and isinstance(json_data, dict):
            if 'action' in json_data:
                result['action'] = json_data['action']
            if 'thought' in json_data and 'thought' not in result:
                result['thought'] = json_data['thought']
            if 'evaluate' in json_data and 'evaluate' not in result:
                result['evaluate'] = json_data['evaluate']

    # === Validation ===
    try:
      return AgentData.model_validate(result)
    except Exception as e:
      _log_extraction_failure(text, result, e)
      raise

def _parse_action_params(raw: str) -> dict[str, Any]:
    """
    Parse action parameters from string.
    Supports JSON, Python dict literal, and other formats.
    """
    if not raw:
        return {}

    raw = raw.strip()

    # Empty object
    if raw in ('{}', 'null', 'None', ''):
        return {}

    # Try JSON
    json_result = ContentExtractor.extract_json(raw)
    if json_result is not None:
        if isinstance(json_result, dict):
            return json_result
        # If not dict returned, wrap it
        return {"value": json_result}

    # Try Python literal (for dict, list, etc.)
    try:
        result = ast.literal_eval(raw)
        if isinstance(result, dict):
            return result
        return {"value": result}
    except (ValueError, SyntaxError):
        pass

    # Last attempt: maybe it's just a string value
    # For example: action_input contains just "click" without JSON
    return {"raw": raw}

def _log_extraction_failure(text: str, result: dict, error: Exception) -> None:
    """Logging extraction error for debugging"""
    separator = "=" * 60
    print(f"\n{separator}")
    print("❌ FAILED TO EXTRACT AGENT DATA")
    print(separator)
    print(f"Error: {type(error).__name__}: {error}")
    print(separator)
    print("📝 Message content:")
    print(text[:1000] + ("..." if len(text) > 1000 else ""))
    print(separator)
    print("📦 Extracted result:")
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    print(f"{separator}\n")

def extract_agent_data_structured(
    llm: BaseChatLLM,
    messages: list[BaseMessage]
) -> AgentData:
    """
    Use structured output instead of XML parsing.
    More reliable for new models.
    """
    response = llm.invoke(
        messages=messages,
        structured_output=AgentData,
    )

    # With structured output, response is already in the right format
    json_data = ContentExtractor.extract_json(response.content)
    return AgentData.model_validate(json_data)

def xml_parser(message: ChatLLMResponse) -> AgentData:
    text = message.content
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

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()
