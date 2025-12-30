from windows_use.llms.google import ChatGoogle
from windows_use.llms.anthropic import ChatAnthropic
from windows_use.llms.ollama import ChatOllama
from windows_use.llms.mistral import ChatMistral
from windows_use.llms.azure_openai import ChatAzureOpenAI
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    api_key = os.getenv("MISTRAL_API_KEY")
    llm=ChatMistral(model='magistral-small-latest',api_key=api_key,temperature=0.7)
    # llm=ChatGoogle(model="gemini-3-flash-preview",thinking_budget=0, api_key=api_key, temperature=0.7)
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
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False, auto_minimize=False)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()