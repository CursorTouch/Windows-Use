from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_cerebras.chat_models import ChatCerebras
from langchain_ollama.chat_models import ChatOllama
from windows_use.agent import Agent, Browser
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    llm = ChatGoogleGenerativeAI(model='gemini-flash-lite-latest', temperature=0.2)
    # llm=ChatCerebras(api_key=os.getenv("CEREBRAS_API_KEY"), model="gpt-oss-120b", temperature=0.2)
    # llm=ChatOllama(model='qwen3-vl:235b-cloud')
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False, auto_minimize=False)
    agent.print_response(query=input("Enter a query: "))

if __name__ == "__main__":
    main()