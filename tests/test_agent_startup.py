import time


def log(msg):
    print(f"[DEBUG] {time.time():.3f}: {msg}", flush=True)


log("Starting main.py debug...")

log("Importing load_dotenv...")
from dotenv import load_dotenv  # noqa: E402

log("Calling load_dotenv...")
load_dotenv()

log("Importing ChatGoogle...")
from windows_use.providers.google import ChatGoogle  # noqa: E402

log("Importing ChatAnthropic...")
log("Importing ChatOllama...")
log("Importing ChatMistral...")
log("Importing ChatAzureOpenAI...")
log("Importing ChatOpenRouter...")
log("Importing ChatGroq...")

log("Importing Agent and Browser...")
from windows_use.agent import Agent, Browser  # noqa: E402


def main():
    log("Inside main()...")
    log("Initializing ChatGoogle...")
    llm = ChatGoogle(model="gemini-2.5-flash-lite", thinking_budget=0, temperature=0.7)

    log("Initializing Agent...")
    agent = Agent(
        llm=llm, browser=Browser.EDGE, use_vision=False, use_annotation=False, auto_minimize=False
    )

    log("Agent initialized. Calling input()...")
    # In a real run, this would be input()
    # But for our test, we'll just simulate it or read from a pipe if needed.
    # We want to see if it even reaches here.
    print("Enter a query: ", end="", flush=True)
    # query = sys.stdin.readline()
    query = "test"
    log(f"Received query: {query}")

    log("Calling agent.print_response...")
    agent.print_response(query=query)
    log("Done.")


if __name__ == "__main__":
    main()
