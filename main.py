from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from windows_use.agent import Agent, Browser
from windows_use.agent.llm import OpenRouterLLM
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # OpenRouter API kullanımı
    if os.getenv("OPENROUTER_API_KEY"):
        print("OpenRouter API kullaniliyor...")
        llm = OpenRouterLLM(
            model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o"),
            temperature=float(os.getenv("OPENROUTER_TEMPERATURE", "0.2")),
            max_tokens=int(os.getenv("OPENROUTER_MAX_TOKENS", "4000")) if os.getenv("OPENROUTER_MAX_TOKENS") else None,
            http_referer=os.getenv("OPENROUTER_HTTP_REFERER"),
            site_title=os.getenv("OPENROUTER_SITE_TITLE")
        )
    # Google Gemini fallback
    elif os.getenv("GOOGLE_API_KEY"):
        print("Google Gemini kullaniliyor...")
        llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0.2)
    else:
        print("Hata: OPENROUTER_API_KEY veya GOOGLE_API_KEY environment variable'i gerekli!")
        print("Lutfen .env dosyasini olusturun ve API anahtarinizi ekleyin.")
        return
    
    agent = Agent(llm=llm, browser=Browser.EDGE, use_vision=False, auto_minimize=True)
    agent.print_response(query=input("görev: "))

if __name__ == "__main__":
    main()