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
    # llm=ChatMistral(model='magistral-small-latest',temperature=0.7)
    # llm=ChatGoogle(model="gemini-2.5-flash-lite",thinking_budget=0, temperature=0.7)
    # llm=ChatOpenRouter(model="nvidia/nemotron-3-nano-30b-a3b:free",temperature=0.2)
    llm=ChatAnthropic(model="claude-sonnet-4-5", temperature=0.7,max_tokens=1000)
    # llm=ChatOllama(model="qwen3-vl:4b",temperature=0.2)
    # llm=ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct",temperature=0.7)
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False,use_annotation=False, auto_minimize=False)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()