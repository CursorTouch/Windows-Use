from windows_use.llms.google import ChatGoogle
from windows_use.llms.anthropic import ChatAnthropic
from windows_use.llms.ollama import ChatOllama
from windows_use.llms.mistral import ChatMistral
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    # llm=ChatMistral(model='magistral-small-latest',api_key=api_key,temperature=0.7)
    llm=ChatGoogle(model="gemini-2.5-flash",thinking_budget=0, api_key=api_key, temperature=0.7)
    # llm=ChatAnthropic(model="claude-sonnet-4-5", api_key=api_key, temperature=0.7,max_tokens=1000)
    # llm=ChatOllama(model="qwen3-vl:235b-cloud",temperature=0.2)
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False, auto_minimize=False)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()