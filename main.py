from windows_use.llm.google import ChatGoogle
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    llm = ChatGoogle(api_key=os.getenv("GOOGLE_API_KEY"),model='gemini-2.5-flash-lite', temperature=0.2)
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False, auto_minimize=True)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()