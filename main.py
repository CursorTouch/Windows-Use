from windows_use.llms.google import ChatGoogle
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    llm=ChatGoogle(model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.7)
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=True, auto_minimize=False)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()