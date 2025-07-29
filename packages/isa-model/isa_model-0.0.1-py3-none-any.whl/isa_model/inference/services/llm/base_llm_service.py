from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union, Optional, AsyncGenerator, TypeVar
from isa_model.inference.services.base_service import BaseService

T = TypeVar('T')  # Generic type for responses

class BaseLLMService(BaseService):
    """Base class for Large Language Model services"""
    
    @abstractmethod
    async def ainvoke(self, prompt: Union[str, List[Dict[str, str]], Any]) -> T:
        """
        Universal invocation method that handles different input types
        
        Args:
            prompt: Can be a string, list of messages, or other format
            
        Returns:
            Model response in the appropriate format
        """
        pass
    
    @abstractmethod
    async def achat(self, messages: List[Dict[str, str]]) -> T:
        """
        Chat completion method using message format
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
                     Example: [{"role": "user", "content": "Hello"}]
            
        Returns:
            Chat completion response
        """
        pass
    
    @abstractmethod
    async def acompletion(self, prompt: str) -> T:
        """
        Text completion method for simple prompt completion
        
        Args:
            prompt: Input text prompt
            
        Returns:
            Text completion response
        """
        pass
    
    @abstractmethod
    async def agenerate(self, messages: List[Dict[str, str]], n: int = 1) -> List[T]:
        """
        Generate multiple completions for the same input
        
        Args:
            messages: List of message dictionaries
            n: Number of completions to generate
            
        Returns:
            List of completion responses
        """
        pass
    
    @abstractmethod
    async def astream_chat(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        """
        Stream chat responses token by token
        
        Args:
            messages: List of message dictionaries
            
        Yields:
            Individual tokens or chunks of the response
        """
        pass
    
    @abstractmethod
    async def astream_completion(self, prompt: str) -> AsyncGenerator[str, None]:
        """
        Stream completion responses token by token
        
        Args:
            prompt: Input text prompt
            
        Yields:
            Individual tokens or chunks of the response
        """
        pass
    
    @abstractmethod
    def get_token_usage(self) -> Dict[str, Any]:
        """
        Get cumulative token usage statistics for this service instance
        
        Returns:
            Dict containing token usage information:
            - total_tokens: Total tokens used
            - prompt_tokens: Tokens used for prompts
            - completion_tokens: Tokens used for completions
            - requests_count: Number of requests made
        """
        pass
    
    @abstractmethod
    def get_last_token_usage(self) -> Dict[str, int]:
        """
        Get token usage from the last request
        
        Returns:
            Dict containing last request token usage:
            - prompt_tokens: Tokens in last prompt
            - completion_tokens: Tokens in last completion
            - total_tokens: Total tokens in last request
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model
        
        Returns:
            Dict containing model information:
            - name: Model name
            - max_tokens: Maximum context length
            - supports_streaming: Whether streaming is supported
            - supports_functions: Whether function calling is supported
        """
        pass
    
    @abstractmethod
    async def close(self):
        """Cleanup resources and close connections"""
        pass
