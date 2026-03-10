import sys
import time
import pytest

def check_import(module_name, from_list=None):
    print(f"Importing {module_name}...", end=" ", flush=True)
    start = time.time()
    try:
        if from_list:
            __import__(module_name, fromlist=from_list)
        else:
            __import__(module_name)
        print(f"Success in {time.time() - start:.2f}s")
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False

@pytest.mark.parametrize("module, from_list", [
    ("dotenv", None),
    ("windows_use.providers.google", ["ChatGoogle"]),
    ("windows_use.providers.anthropic", ["ChatAnthropic"]),
    ("windows_use.providers.ollama", ["ChatOllama"]),
    ("windows_use.providers.mistral", ["ChatMistral"]),
    ("windows_use.providers.azure_openai", ["ChatAzureOpenAI"]),
    ("windows_use.providers.open_router", ["ChatOpenRouter"]),
    ("windows_use.providers.groq", ["ChatGroq"]),
    ("windows_use.agent", ["Agent", "Browser"]),
])
def test_all_imports(module, from_list):
    assert check_import(module, from_list)
