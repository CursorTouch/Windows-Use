import pytest
import json
from unittest.mock import MagicMock, AsyncMock, patch

from windows_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall
from windows_use.providers.openai.llm import ChatOpenAI
from windows_use.messages import HumanMessage

def create_mock_chunk(content=None, tool_calls=None, reasoning=None):
    delta = MagicMock()
    delta.content = content
    delta.reasoning_content = reasoning
    
    if tool_calls:
        delta.tool_calls = []
        for tc in tool_calls:
            mock_tc = MagicMock()
            mock_tc.id = tc.get("id")
            mock_tc.function = MagicMock()
            mock_tc.function.name = tc.get("name")
            mock_tc.function.arguments = tc.get("arguments")
            delta.tool_calls.append(mock_tc)
    else:
        delta.tool_calls = None

    choice = MagicMock()
    choice.delta = delta

    chunk = MagicMock()
    chunk.choices = [choice]
    chunk.usage = None
    return chunk

def test_stream_text_only():
    provider = ChatOpenAI(model="gpt-4o")
    
    mock_chunks = [
        create_mock_chunk(content="Hello"),
        create_mock_chunk(content=" world"),
        create_mock_chunk(content="!")
    ]
    
    provider.client.chat.completions.create = MagicMock(return_value=mock_chunks)
    
    events = list(provider.stream([HumanMessage(content="test")]))
    
    assert len(events) == 5
    assert events[0] == LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
    assert events[1] == LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content="Hello")
    assert events[2] == LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=" world")
    assert events[3] == LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content="!")
    assert events[4] == LLMStreamEvent(type=LLMStreamEventType.TEXT_END)

def test_stream_tool_only():
    provider = ChatOpenAI(model="gpt-4o")
    
    mock_chunks = [
        create_mock_chunk(tool_calls=[{"id": "call_123", "name": "my_tool", "arguments": '{"arg"'} ]),
        create_mock_chunk(tool_calls=[{"id": None, "name": None, "arguments": ':"val"'} ]),
        create_mock_chunk(tool_calls=[{"id": None, "name": None, "arguments": '}'} ])
    ]
    
    provider.client.chat.completions.create = MagicMock(return_value=mock_chunks)
    
    events = list(provider.stream([HumanMessage(content="test")]))
    
    assert len(events) == 1
    assert events[0].type == LLMStreamEventType.TOOL_CALL
    assert events[0].tool_call is not None
    assert events[0].tool_call.id == "call_123"
    assert events[0].tool_call.name == "my_tool"
    assert events[0].tool_call.params == {"arg": "val"}

def test_stream_thinking_then_text():
    provider = ChatOpenAI(model="o3-mini")
    
    mock_chunks = [
        create_mock_chunk(reasoning="Thinking"),
        create_mock_chunk(reasoning="..."),
        create_mock_chunk(content="Done thinking."),
    ]
    
    provider.client.chat.completions.create = MagicMock(return_value=mock_chunks)
    
    events = list(provider.stream([HumanMessage(content="test")]))
    
    assert len(events) == 7
    assert events[0] == LLMStreamEvent(type=LLMStreamEventType.THINK_START)
    assert events[1] == LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content="Thinking")
    assert events[2] == LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content="...")
    assert events[3] == LLMStreamEvent(type=LLMStreamEventType.THINK_END)
    assert events[4] == LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
    assert events[5] == LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content="Done thinking.")
    assert events[6] == LLMStreamEvent(type=LLMStreamEventType.TEXT_END)
