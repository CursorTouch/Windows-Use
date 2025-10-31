from windows_use.llms.google import ChatGoogle
from windows_use.llms.ollama import ChatOllama
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    llm=ChatGoogle(model="gemini-2.5-flash-lite", api_key=api_key, temperature=0.7)
    # llm=ChatOllama(model="qwen3-vl:235b-cloud",temperature=0.2)
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=True, auto_minimize=True)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()