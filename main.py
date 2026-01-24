from windows_use.llms.google import ChatGoogle
from windows_use.llms.anthropic import ChatAnthropic
from windows_use.llms.ollama import ChatOllama
from windows_use.llms.mistral import ChatMistral
from windows_use.llms.azure_openai import ChatAzureOpenAI
from windows_use.llms.open_router import ChatOpenRouter
from windows_use.llms.groq import ChatGroq
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    llm=ChatMistral(model='magistral-small-latest',temperature=0.7)
    # llm=ChatGoogle(model="gemini-2.5-flash-lite",thinking_budget=0, temperature=0.7)
    # llm=ChatOpenRouter(model="xiaomi/mimo-v2-flash:free",temperature=0.2)
    # llm=ChatAnthropic(model="claude-sonnet-4-5", temperature=0.7,max_tokens=1000)
    # llm=ChatOllama(model="qwen3-vl:235b-cloud",temperature=0.2)
    # llm=ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct",temperature=0.7, json_mode=True)
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False,use_annotation=False, auto_minimize=False)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()