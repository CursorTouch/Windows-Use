<div align="center">

  <h1>🪟 Windows-Use</h1>
  <a href="https://pepy.tech/project/windows-use">
    <img src="https://static.pepy.tech/badge/windows-use" alt="PyPI Downloads">
  </a>
  <a href="https://github.com/CursorTouch/windows-use/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  </a>
  <img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python">
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

**Windows-Use** is a powerful automation agent that interact directly with the Windows at GUI layer. It bridges the gap between AI Agents and the Windows OS to perform tasks such as opening apps, clicking buttons, typing, executing shell commands, and capturing UI state all without relying on traditional computer vision models. Enabling any LLM to perform computer automation instead of relying on specific models for it.

## 🛠️Installation Guide

### **Prerequisites**

- Python 3.12 or higher
- [UV](https://github.com/astral-sh/uv) (or `pip`)
- Windows 7 or 8 or 10 or 11

### **Installation Steps**

**Install using `uv`:**

```bash
uv pip install windows-use
````

Or with pip:

```bash
pip install windows-use
```

## ⚙️Basic Usage


### Ollama

```python
from windows_use.llm.ollama import ChatOllama
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    llm=ChatOllama(model='qwen3-vl:235b-cloud')
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False, auto_minimize=False)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()
```

### Google Gemini

```python
from windows_use.llm.google import ChatGoogle
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    llm = ChatGoogle(model='gemini-2.5-flash', temperature=0.2)
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False, auto_minimize=True)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()
```

## 🤖 Run Agent

You can use the following to run from a script:

```bash
python main.py
```

---

## 🎥 Demos

**PROMPT:** Write a short note about LLMs and save to the desktop

<https://github.com/user-attachments/assets/0faa5179-73c1-4547-b9e6-2875496b12a0>

**PROMPT:** Change from Dark mode to Light mode

<https://github.com/user-attachments/assets/47bdd166-1261-4155-8890-1b2189c0a3fd>

## 📈 Grounding

![Image](https://github.com/user-attachments/assets/e1d32725-e28a-4821-9c89-24b5ba2e583f)
![Image](https://github.com/user-attachments/assets/be72ad43-c320-4831-95cf-6f1f30df18de)
![Image](https://github.com/user-attachments/assets/d91b513e-13a0-4451-a6e9-f1e16def36e3)
![Image](https://github.com/user-attachments/assets/7e832999-0fce-4d26-b884-cff17aa91073)
![Image](https://github.com/user-attachments/assets/87a7d775-c51f-494c-be73-cfd7e8282f8e)

## Vision

Talk to your computer. Watch it get things done.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CursorTouch/Windows-Use&type=Date)](https://www.star-history.com/#CursorTouch/Windows-Use&Date)

## ⚠️ Caution

Agent interacts directly with your Windows OS at GUI layer to perform actions. While the agent is designed to act intelligently and safely, it can make mistakes that might bring undesired system behaviour or cause unintended changes. Try to run the agent in a sandbox envirnoment.

## 🪪 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

Windows-Use makes use of several excellent open-source projects that power its Windows automation features:

- [UIAutomation](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows)

- [PyAutoGUI](https://github.com/asweigart/pyautogui)

Huge thanks to the maintainers and contributors of these libraries for their outstanding work and open-source spirit.

## 🤝 Contributing

Contributions are welcome! Please check the [CONTRIBUTING](CONTRIBUTING) file for setup and development workflow.

Made with ❤️ by [Jeomon George](https://github.com/Jeomon)

---

## Citation

```bibtex
@software{
  author       = {George, Jeomon},
  title        = {Windows-Use: Enable AI to control Windows OS},
  year         = {2025},
  publisher    = {GitHub},
  url={https://github.com/CursorTouch/Windows-Use}
}
```
