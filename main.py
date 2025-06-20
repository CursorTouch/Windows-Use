from langchain_google_genai import ChatGoogleGenerativeAI
from windows_use.agent import Agent
from dotenv import load_dotenv

load_dotenv()

llm=ChatGoogleGenerativeAI(model='gemini-2.0-flash')
agent = Agent(llm=llm,use_vision=True,max_steps=100)
query=input("Enter your query: ")
agent_result=agent.invoke(query=query)
print(agent_result.content)