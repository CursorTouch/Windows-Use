<div align="center">

  <h1>🪟 Windows-Use</h1>
  <a href="https://pepy.tech/project/windows-use">
    <img src="https://static.pepy.tech/badge/windows-use" alt="PyPI Downloads">
  </a>
  <a href="https://github.com/CursorTouch/windows-use/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  </a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows%207–11-blue" alt="Platform: Windows 7 to 11">
  <br>

  <a href="https://x.com/CursorTouch">
    <img src="https://img.shields.io/badge/follow-%40CursorTouch-1DA1F2?logo=twitter&style=flat" alt="Follow on Twitter">
  </a>
  <a href="https://discord.com/invite/Aue9Yj2VzS">
    <img src="https://img.shields.io/badge/Join%20on-Discord-5865F2?logo=discord&logoColor=white&style=flat" alt="Join us on Discord">
  </a>

</div>

<br>

**Windows-Use** is an AI agent that controls Windows at the GUI layer. It reads the screen via the Windows UI Automation API and uses any LLM to decide what to click, type, scroll, or run — no computer vision model required.

Give it a task in plain English. It handles the rest.

## What It Can Do

- Open, switch between, and resize application windows
- Click, type, scroll, drag, and use keyboard shortcuts
- Run PowerShell commands and read their output
- Scrape web pages via the browser accessibility tree
- Read and write files on the filesystem
- Manage Windows virtual desktops (create, rename, switch)
- Remember information across steps with persistent memory
- Speak and listen via STT/TTS (voice input and output)

## 🛠️ Installation

**Prerequisites:** Python 3.10+, Windows 7/8/10/11

```bash
pip install windows-use
```

Or with `uv`:

```bash
uv add windows-use
```

## ⚙️ Quick Start

Pick any supported LLM provider and run a task:

### Anthropic (Claude)

```python
from windows_use.providers.anthropic import ChatAnthropic
from windows_use import Agent, Browser

llm = ChatAnthropic(model="claude-sonnet-4-5")
agent = Agent(llm=llm, browser=Browser.EDGE)
agent.invoke(task="Open Notepad and write a short poem about Windows")
```

### OpenAI

```python
from windows_use.providers.openai import ChatOpenAI
from windows_use import Agent, Browser

llm = ChatOpenAI(model="gpt-4o")
agent = Agent(llm=llm, browser=Browser.CHROME)
agent.invoke(task="Search for the weather in New York on Google")
```

### Google Gemini

```python
from windows_use.providers.google import ChatGoogle
from windows_use import Agent, Browser

llm = ChatGoogle(model="gemini-2.5-flash")
agent = Agent(llm=llm, browser=Browser.EDGE)
agent.invoke(task=input("Enter a task: "))
```

### Ollama (Local)

```python
from windows_use.providers.ollama import ChatOllama
from windows_use import Agent, Browser

llm = ChatOllama(model="qwen3-vl:235b-cloud")
agent = Agent(llm=llm, use_vision=False)
agent.invoke(task=input("Enter a task: "))
```

### Async Usage

```python
import asyncio
from windows_use.providers.anthropic import ChatAnthropic
from windows_use import Agent

async def main():
    llm = ChatAnthropic(model="claude-sonnet-4-5")
    agent = Agent(llm=llm)
    result = await agent.ainvoke(task="Take a screenshot and describe the desktop")
    print(result.content)

asyncio.run(main())
```

## 🤖 CLI

Run the interactive agent directly from your terminal:

```bash
windows-use
```

**Options:**

```
--model, -m      LLM model to use
--provider, -p   LLM provider
--max-steps      Max steps per task (default: 200)
--debug, -d      Enable debug logging
```

**In-session commands:**

| Command   | Description                  |
|-----------|------------------------------|
| `\llm`    | Switch provider or model     |
| `\key`    | Change API key               |
| `\speech` | Configure STT/TTS            |
| `\voice`  | Record voice input           |
| `\clear`  | Clear the screen             |
| `\quit`   | Exit                         |

## 🔌 Supported LLM Providers

| Provider     | Import                                        |
|--------------|-----------------------------------------------|
| Anthropic    | `from windows_use.providers.anthropic import ChatAnthropic` |
| OpenAI       | `from windows_use.providers.openai import ChatOpenAI`       |
| Google       | `from windows_use.providers.google import ChatGoogle`       |
| Groq         | `from windows_use.providers.groq import ChatGroq`           |
| Ollama       | `from windows_use.providers.ollama import ChatOllama`       |
| Mistral      | `from windows_use.providers.mistral import ChatMistral`     |
| Cerebras     | `from windows_use.providers.cerebras import ChatCerebras`   |
| DeepSeek     | `from windows_use.providers.deepseek import ChatDeepSeek`   |
| Azure OpenAI | `from windows_use.providers.azure_openai import ChatAzureOpenAI` |
| Open Router  | `from windows_use.providers.open_router import ChatOpenRouter`   |
| LiteLLM      | `from windows_use.providers.litellm import ChatLiteLLM`     |
| NVIDIA       | `from windows_use.providers.nvidia import ChatNvidia`       |
| vLLM         | `from windows_use.providers.vllm import ChatVLLM`           |

## 🧰 Agent Configuration

```python
Agent(
    llm=llm,                        # LLM instance (required)
    mode="normal",                  # "normal" (full context) or "flash" (lightweight, faster)
    browser=Browser.EDGE,           # Browser.EDGE | Browser.CHROME | Browser.FIREFOX
    use_vision=False,               # Send screenshots to the LLM
    use_annotation=False,           # Annotate UI elements on screenshots
    use_accessibility=True,         # Use the Windows accessibility tree
    auto_minimize=False,            # Minimize active window before the agent starts
    max_steps=25,                   # Max number of steps before giving up
    max_consecutive_failures=3,     # Abort after N consecutive tool failures
    instructions=[],                # Extra system instructions
    secrets={},                     # Key-value secrets passed to the agent context
    log_to_console=True,            # Print steps to the console
    log_to_file=False,              # Write steps to a log file
    event_subscriber=None,          # Custom event listener (see Events section)
    experimental=False,             # Enable experimental tools (file, memory, multi-select)
)
```

**Tip:** Use `claude-haiku-4-*`, `claude-sonnet-4-*`, or `claude-opus-4-*` for best results.

## 🛠️ Tools

The agent has access to these tools automatically — no configuration needed.

**Core Tools:**

| Tool             | Description                                              |
|------------------|----------------------------------------------------------|
| `click_tool`     | Left, right, middle click or hover at coordinates       |
| `type_tool`      | Type text into any input field                          |
| `scroll_tool`    | Scroll vertically or horizontally                       |
| `move_tool`      | Move mouse or drag-and-drop                             |
| `shortcut_tool`  | Press keyboard shortcuts (e.g. `ctrl+c`, `alt+tab`)    |
| `app_tool`       | Launch, switch, or resize application windows           |
| `shell_tool`     | Run PowerShell commands                                 |
| `scrape_tool`    | Extract text content from web pages                     |
| `desktop_tool`   | Create, rename, switch Windows virtual desktops         |
| `wait_tool`      | Pause execution for N seconds                           |
| `done_tool`      | Return the final answer to the user                     |

**Experimental Tools** (enable with `experimental=True`):

| Tool               | Description                                            |
|--------------------|--------------------------------------------------------|
| `file_tool`        | Read, write, list, move, copy, delete files            |
| `memory_tool`      | Persist information across steps in markdown files     |
| `multi_select_tool`| Ctrl+click multiple elements at once                  |
| `multi_edit_tool`  | Fill multiple form fields in one action               |

## 📡 Events

Observe every step the agent takes with the event system:

```python
from windows_use import Agent, AgentEvent, EventType, BaseEventSubscriber

class MySubscriber(BaseEventSubscriber):
    def invoke(self, event: AgentEvent):
        if event.type == EventType.TOOL_CALL:
            print(f"Tool: {event.data['tool_name']}")
        elif event.type == EventType.DONE:
            print(f"Done: {event.data['answer']}")

agent = Agent(llm=llm, event_subscriber=MySubscriber())
```

Or use a plain callable:

```python
def on_event(event: AgentEvent):
    print(f"{event.type.value}: {event.data}")

agent = Agent(llm=llm, event_subscriber=on_event)
```

**Event types:** `THOUGHT` · `TOOL_CALL` · `TOOL_RESULT` · `DONE` · `ERROR`

## 🎙️ Voice (STT / TTS)

Windows-Use supports voice input and spoken output via multiple providers.

**STT (Speech-to-Text):** OpenAI Whisper · Google · Groq · ElevenLabs · Deepgram

**TTS (Text-to-Speech):** OpenAI · Google · Groq · ElevenLabs · Deepgram

```python
from windows_use.providers.openai import ChatOpenAI, STTOpenAI, TTSOpenAI
from windows_use.speech import STT, TTS

llm = ChatOpenAI(model="gpt-4o")
stt = STT(provider=STTOpenAI())
tts = TTS(provider=TTSOpenAI())

task = stt.invoke()              # Record and transcribe voice input
agent = Agent(llm=llm)
result = agent.invoke(task=task)
tts.invoke(result.content)       # Speak the response aloud
```

## 🖥️ Virtual Desktops

The agent can manage Windows virtual desktops natively:

```python
from windows_use.vdm.core import create_desktop, switch_desktop, remove_desktop

create_desktop("Work")
switch_desktop("Work")
remove_desktop("Work")
```

Supported on Windows 10 (build 17763+) and all Windows 11 versions.

## ⚠️ Security

This agent can:
- Operate your computer on behalf of the user
- Modify files and system settings
- Make irreversible changes to your system

**⚠️ STRONGLY RECOMMENDED: Deploy in a Virtual Machine or Windows Sandbox**

The project provides **NO sandbox or isolation layer**. For your safety:
- ✅ Use a Virtual Machine (VirtualBox, VMware, Hyper-V)
- ✅ Use Windows Sandbox (Windows 10/11 Pro/Enterprise)
- ✅ Use a dedicated test machine

**📖 Read the full [Security Policy](SECURITY.md) before deployment.**

## 📡 Telemetry

Windows-Use includes lightweight, privacy-friendly telemetry to help improve reliability and understand real-world usage.

Disable it at any time:

```env
ANONYMIZED_TELEMETRY=false
```

Or in code:

```python
import os
os.environ["ANONYMIZED_TELEMETRY"] = "false"
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Jeomon/Windows-Use&type=Date)](https://www.star-history.com/?repos=Jeomon%2FWindows-Use&type=date&legend=top-left)

## 🪪 License

MIT — see [LICENSE](LICENSE).

## 🙏 Acknowledgements

- [UIAutomation](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows)
- [PyAutoGUI](https://github.com/asweigart/pyautogui)

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING](CONTRIBUTING) for the development workflow.

Made with ❤️ by [Jeomon George](https://github.com/Jeomon)

---

## Citation

```bibtex
@software{
  author       = {George, Jeomon},
  title        = {Windows-Use: Enable AI to control Windows OS},
  year         = {2025},
  publisher    = {GitHub},
  url          = {https://github.com/CursorTouch/Windows-Use}
}
```
