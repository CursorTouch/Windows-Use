"""
OpenRouter API entegrasyonu için LangChain uyumlu LLM sınıfı
"""
import requests
import json
from typing import Any, Dict, List, Optional, Iterator
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()


class OpenRouterLLM(BaseChatModel):
    """
    OpenRouter API için LangChain uyumlu LLM sınıfı
    """
    
    api_key: str = Field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))
    base_url: str = Field(default="https://openrouter.ai/api/v1/chat/completions")
    model: str = Field(default="openai/gpt-4o")
    temperature: float = Field(default=0.2)
    max_tokens: Optional[int] = Field(default=None)
    http_referer: Optional[str] = Field(default=None)
    site_title: Optional[str] = Field(default=None)
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """OpenRouter API'ye istek gönder ve yanıt al"""
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        # LangChain mesajlarını OpenRouter formatına dönüştür
        openrouter_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                openrouter_messages.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                openrouter_messages.append({"role": "assistant", "content": message.content})
            elif isinstance(message, SystemMessage):
                openrouter_messages.append({"role": "system", "content": message.content})
        
        # API isteği için payload hazırla
        payload = {
            "model": self.model,
            "messages": openrouter_messages,
            "temperature": self.temperature,
        }
        
        if self.max_tokens:
            payload["max_tokens"] = self.max_tokens
            
        if stop:
            payload["stop"] = stop
            
        # Headers hazırla
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        if self.http_referer:
            headers["HTTP-Referer"] = self.http_referer
        if self.site_title:
            headers["X-Title"] = self.site_title
            
        try:
            # API isteği gönder
            response = requests.post(
                self.base_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            
            # Yanıtı işle
            response_data = response.json()
            
            if "choices" not in response_data or not response_data["choices"]:
                raise ValueError("Invalid response from OpenRouter API")
                
            choice = response_data["choices"][0]
            content = choice["message"]["content"]
            
            # Emoji karakterlerini temizle (Windows encoding sorunları için)
            try:
                content = content.encode('ascii', 'ignore').decode('ascii')
            except:
                pass
            
            # LangChain formatına dönüştür
            message = AIMessage(content=content)
            generation = ChatGeneration(message=message)
            
            return ChatResult(generations=[generation])
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"OpenRouter API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise ValueError(f"Invalid response format from OpenRouter API: {str(e)}")
    
    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGeneration]:
        """Streaming desteği - şimdilik desteklenmiyor"""
        # Streaming henüz desteklenmiyor, normal generate kullan
        result = self._generate(messages, stop, run_manager, **kwargs)
        yield result.generations[0]
    
    @property
    def _llm_type(self) -> str:
        return "openrouter"
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
