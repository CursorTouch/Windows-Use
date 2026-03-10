import os
import sys
import time

def log(msg):
    print(f"[DEBUG] {time.time():.3f}: {msg}", flush=True)

log("Starting main.py debug...")

log("Importing load_dotenv...")
from dotenv import load_dotenv
log("Calling load_dotenv...")
load_dotenv()

log("Importing ChatGoogle...")
from windows_use.providers.google import ChatGoogle
log("Importing ChatAnthropic...")
from windows_use.providers.anthropic import ChatAnthropic
log("Importing ChatOllama...")
from windows_use.providers.ollama import ChatOllama
log("Importing ChatMistral...")
from windows_use.providers.mistral import ChatMistral
log("Importing ChatAzureOpenAI...")
from windows_use.providers.azure_openai import ChatAzureOpenAI
log("Importing ChatOpenRouter...")
from windows_use.providers.open_router import ChatOpenRouter
log("Importing ChatGroq...")
from windows_use.providers.groq import ChatGroq

log("Importing Agent and Browser...")
from windows_use.agent import Agent, Browser

def main():
    log("Inside main()...")
    log("Initializing ChatGoogle...")
    llm=ChatGoogle(model="gemini-2.5-flash-lite",thinking_budget=0, temperature=0.7)
    
    log("Initializing Agent...")
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False,use_annotation=False, auto_minimize=False)
    
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
