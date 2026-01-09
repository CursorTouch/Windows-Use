from windows_use.llms.google import ChatGoogle
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    # llm=ChatMistral(model='magistral-small-latest',api_key=api_key,temperature=0.0, profile="deterministic")
    # Some external ChatGoogle implementations may not accept `profile`.
    # Use a backward-compatible call without `profile` to avoid TypeError.
    llm=ChatGoogle(model="gemini-2.5-flash", api_key=api_key, temperature=0.0)
    # llm=ChatAnthropic(model="claude-sonnet-4-5", api_key=api_key, temperature=0.7,max_tokens=1000)
    # llm=ChatOllama(model="qwen3-vl:235b-cloud",temperature=0.2)
    # llm=ChatAzureOpenAI(
    #     endpoint=os.getenv("AOAI_ENDPOINT"),
    #     deployment_name=os.getenv("AOAI_DEPLOYMENT_NAME"),
    #     api_key=os.getenv("AOAI_API_KEY"),
    #     model=os.getenv("AOAI_MODEL"),
    #     api_version=os.getenv("AOAI_API_VERSION", "2025-01-01-preview"),
    #     temperature=0.7
    # )
    # Configure agent for deterministic, low-latency operation: fewer retries and steps.
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False, auto_minimize=True, max_consecutive_failures=1, max_steps=10)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()