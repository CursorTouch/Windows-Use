import asyncio
import os
import sys

from windows_use.providers.openai.llm import ChatOpenAI
from windows_use.providers.events import LLMEvent, LLMEventType
from windows_use.messages import HumanMessage, AIMessage, ToolMessage
from windows_use.tools import Tool


from pydantic import BaseModel

class DummyToolModel(BaseModel):
    dummy: str

dummy_tool = Tool(
    name="dummy_tool",
    description="A dummy tool for testing",
    model=DummyToolModel
)

async def test_streaming_text():
    print("=== Testing Streaming Text ===")
    llm = ChatOpenAI(model="gpt-4o-mini", max_retries=1)
    
    # MOCK OPENAI STREAM
    from unittest.mock import MagicMock
    class MockDelta:
        def __init__(self, content=None, reasoning_content=None, tool_calls=None):
            self.content = content
            self.reasoning_content = reasoning_content
            self.tool_calls = tool_calls

    class MockChoice:
        def __init__(self, delta):
            self.delta = delta

    class MockChunk:
        def __init__(self, choices, usage=None):
            self.choices = choices
            self.usage = usage

    def mock_stream(*args, **kwargs):
        yield MockChunk([MockChoice(MockDelta(reasoning_content="I should think about this..."))])
        yield MockChunk([MockChoice(MockDelta(content="Hello!"))])
        yield MockChunk([MockChoice(MockDelta(content=" World"))])
        yield MockChunk([], usage=MagicMock(prompt_tokens=10, completion_tokens=5, total_tokens=15))

    llm.client.chat.completions.create = mock_stream
    llm._is_reasoning_model = lambda: True

    events_received = []
    
    # Simple message
    messages = [HumanMessage(content="Explain what a computer is in 2 short sentences.")]
    
    for chunk in llm.stream(messages=messages):
        assert isinstance(chunk, LLMEvent), f"Expected LLMEvent, got {type(chunk).__name__}"
        print(f"[EVENT] {chunk.type.value}: {chunk.content or chunk.tool_name or chunk.tool_params}")
        events_received.append(chunk.type)
    
    assert LLMEventType.TEXT_START in events_received
    assert LLMEventType.TEXT_DELTA in events_received
    assert LLMEventType.TEXT_END in events_received
    print("SUCCESS: Text stream generated start, delta, and end events.")


async def test_streaming_tools():
    print("\n=== Testing Streaming Tools ===")
    llm = ChatOpenAI(model="gpt-4o-mini", max_retries=1)
    
    # MOCK OPENAI STREAM
    from unittest.mock import MagicMock
    class MockToolFunction:
        def __init__(self, name=None, arguments=None):
            self.name = name
            self.arguments = arguments

    class MockToolCall:
        def __init__(self, id=None, function=None):
            self.id = id
            self.function = function

    class MockDelta:
        def __init__(self, tool_calls=None, content=None):
            self.tool_calls = tool_calls
            self.content = content

    class MockChoice:
        def __init__(self, delta):
            self.delta = delta

    class MockChunk:
        def __init__(self, choices, usage=None):
            self.choices = choices
            self.usage = usage

    def mock_stream(*args, **kwargs):
        t1 = MockToolCall(id="call_abc", function=MockToolFunction(name="dummy_tool", arguments='{"dum'))
        t2 = MockToolCall(function=MockToolFunction(arguments='my": "hello"}'))
        yield MockChunk([MockChoice(MockDelta(tool_calls=[t1]))])
        yield MockChunk([MockChoice(MockDelta(tool_calls=[t2]))])
        yield MockChunk([], usage=MagicMock(prompt_tokens=10, completion_tokens=5, total_tokens=15))

    llm.client.chat.completions.create = mock_stream
    llm._is_reasoning_model = lambda: False
    
    events_received = []
    
    messages = [HumanMessage(content="Call the dummy tool with the argument 'hello'.")]
    
    for chunk in llm.stream(messages=messages, tools=[dummy_tool]):
        assert isinstance(chunk, LLMEvent), f"Expected LLMEvent, got {type(chunk).__name__}"
        print(f"[EVENT] {chunk.type.value}: {chunk.tool_name} {chunk.tool_params}")
        events_received.append(chunk.type)
    
    assert LLMEventType.TOOL_CALL in events_received
    print("SUCCESS: Tool stream generated start, delta, and end events.")


async def test_invoke_text():
    print("\n=== Testing Invoke Text ===")
    llm = ChatOpenAI(model="gpt-4o-mini", max_retries=1)
    
    # MOCK OPENAI INVOKE
    from unittest.mock import MagicMock
    class MockMessage:
        def __init__(self, content=None, tool_calls=None):
            self.content = content
            self.tool_calls = tool_calls

    class MockChoice:
        def __init__(self, message):
            self.message = message

    class MockResponse:
        def __init__(self, choices, usage=None):
            self.choices = choices
            self.usage = usage

    def mock_create(*args, **kwargs):
        return MockResponse([MockChoice(MockMessage(content="Invoke Hello!"))], usage=MagicMock(prompt_tokens=10, completion_tokens=5, total_tokens=15))

    llm.client.chat.completions.create = mock_create
    llm._is_reasoning_model = lambda: False
    
    messages = [HumanMessage(content="Say Hello via invoke")]
    result = llm.invoke(messages=messages)
    
    assert isinstance(result, LLMEvent), f"Expected LLMEvent from invoke, got {type(result).__name__}"
    assert result.type == LLMEventType.TEXT_END
    assert result.content == "Invoke Hello!"
    print(f"[INVOKE EVENT] {result.type.value}: {result.content}")
    print("SUCCESS: Invoke text generated TEXT_END LLMEvent.")

async def test_ainvoke_tools():
    print("\n=== Testing Ainvoke Tools ===")
    llm = ChatOpenAI(model="gpt-4o-mini", max_retries=1)
    
    # MOCK OPENAI AINVOKE
    from unittest.mock import MagicMock
    class MockToolFunction:
        def __init__(self, name=None, arguments=None):
            self.name = name
            self.arguments = arguments

    class MockToolCall:
        def __init__(self, id=None, function=None):
            self.id = id
            self.function = function

    class MockMessage:
        def __init__(self, content=None, tool_calls=None):
            self.content = content
            self.tool_calls = tool_calls

    class MockChoice:
        def __init__(self, message):
            self.message = message

    class MockResponse:
        def __init__(self, choices, usage=None):
            self.choices = choices
            self.usage = usage

    async def mock_acreate(*args, **kwargs):
        t1 = MockToolCall(id="call_123", function=MockToolFunction(name="dummy_tool", arguments='{"dummy": "world"}'))
        return MockResponse([MockChoice(MockMessage(tool_calls=[t1]))], usage=MagicMock(prompt_tokens=10, completion_tokens=5, total_tokens=15))

    llm.aclient.chat.completions.create = mock_acreate
    llm._is_reasoning_model = lambda: False
    
    messages = [HumanMessage(content="Call the dummy tool with 'world'")]
    result = await llm.ainvoke(messages=messages, tools=[dummy_tool])
    
    assert isinstance(result, LLMEvent), f"Expected LLMEvent from ainvoke, got {type(result).__name__}"
    assert result.type == LLMEventType.TOOL_CALL
    assert result.tool_name == "dummy_tool"
    assert "world" in result.tool_params
    print(f"[AINVOKE EVENT] {result.type.value}: {result.tool_name} {result.tool_params}")
    print("SUCCESS: Ainvoke tools generated TOOL_CALL_END LLMEvent.")

async def main():
    await test_streaming_text()
    await test_streaming_tools()
    await test_invoke_text()
    await test_ainvoke_tools()

if __name__ == "__main__":
    asyncio.run(main())
