import logging
import os
from typing import Dict, Any, List, Union, AsyncGenerator, Optional

# 使用官方 OpenAI 库和 dotenv
from openai import AsyncOpenAI
from dotenv import load_dotenv

from isa_model.inference.services.base_service import BaseLLMService
from isa_model.inference.providers.base_provider import BaseProvider

# 加载 .env.local 文件中的环境变量
load_dotenv(dotenv_path='.env.local')

logger = logging.getLogger(__name__)

class OpenAILLMService(BaseLLMService):
    """OpenAI LLM service implementation"""
    
    def __init__(self, provider: 'BaseProvider', model_name: str = "gpt-3.5-turbo"):
        super().__init__(provider, model_name)
        
        # 从provider配置初始化 AsyncOpenAI 客户端
        try:
            api_key = provider.config.get("api_key") or os.getenv("OPENAI_API_KEY")
            base_url = provider.config.get("api_base") or os.getenv("OPENAI_API_BASE")
            
            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url=base_url
            )
        except TypeError as e:
            logger.error("初始化 OpenAI 客户端失败。请检查您的 .env.local 文件中是否正确设置了 OPENAI_API_KEY。")
            raise ValueError("OPENAI_API_KEY 未设置。") from e
            
        self.last_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        logger.info(f"Initialized OpenAILLMService with model {self.model_name} and endpoint {self.client.base_url}")
    
    async def ainvoke(self, prompt: Union[str, List[Dict[str, str]], Any]) -> str:
        """Universal invocation method"""
        if isinstance(prompt, str):
            return await self.acompletion(prompt)
        elif isinstance(prompt, list):
            return await self.achat(prompt)
        else:
            raise ValueError("Prompt must be a string or a list of messages")
    
    async def achat(self, messages: List[Dict[str, str]]) -> str:
        """Chat completion method"""
        try:
            temperature = self.config.get("temperature", 0.7)
            max_tokens = self.config.get("max_tokens", 1024)
            
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            if response.usage:
                self.last_token_usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise
    
    async def acompletion(self, prompt: str) -> str:
        """Text completion method (using chat API)"""
        messages = [{"role": "user", "content": prompt}]
        return await self.achat(messages)
    
    async def agenerate(self, messages: List[Dict[str, str]], n: int = 1) -> List[str]:
        """Generate multiple completions"""
        try:
            temperature = self.config.get("temperature", 0.7)
            max_tokens = self.config.get("max_tokens", 1024)
            
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                n=n
            )
            
            if response.usage:
                self.last_token_usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            
            return [choice.message.content or "" for choice in response.choices]
        except Exception as e:
            logger.error(f"Error in generate: {e}")
            raise
    
    async def astream_chat(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        """Stream chat responses"""
        try:
            temperature = self.config.get("temperature", 0.7)
            max_tokens = self.config.get("max_tokens", 1024)
            
            stream = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
                
        except Exception as e:
            logger.error(f"Error in stream chat: {e}")
            raise
    
    def get_token_usage(self) -> Dict[str, int]:
        """Get total token usage statistics"""
        return self.last_token_usage
    
    def get_last_token_usage(self) -> Dict[str, int]:
        """Get token usage from last request"""
        return self.last_token_usage
        
    async def close(self):
        """Close the backend client"""
        await self.client.aclose()