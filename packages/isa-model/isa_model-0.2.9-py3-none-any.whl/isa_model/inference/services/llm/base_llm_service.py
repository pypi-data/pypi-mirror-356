from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union, Optional, AsyncGenerator, TypeVar, Callable
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
    
    def bind_tools(self, tools: List[Union[Dict[str, Any], Callable]], **kwargs) -> 'BaseLLMService':
        """
        Bind tools to this LLM service for function calling (LangChain interface)
        
        Args:
            tools: List of tools to bind. Can be:
                  - Dictionary with tool schema
                  - Callable functions (will be converted to schema)
            **kwargs: Additional tool binding parameters
            
        Returns:
            A new instance of the service with tools bound
            
        Example:
            def get_weather(location: str) -> str:
                '''Get weather for a location'''
                return f"Weather in {location}: Sunny, 25°C"
            
            llm_with_tools = llm.bind_tools([get_weather])
            response = await llm_with_tools.ainvoke("What's the weather in Paris?")
        """
        # Create a copy of the current service
        bound_service = self._create_bound_copy()
        bound_service._bound_tools = self._convert_tools_to_schema(tools)
        bound_service._tool_binding_kwargs = kwargs
        return bound_service
    
    def _create_bound_copy(self) -> 'BaseLLMService':
        """Create a copy of this service for tool binding"""
        # Default implementation - subclasses should override if needed
        bound_service = self.__class__(self.provider, self.model_name)
        bound_service.config = self.config.copy()
        return bound_service
    
    def _convert_tools_to_schema(self, tools: List[Union[Dict[str, Any], Callable]]) -> List[Dict[str, Any]]:
        """Convert tools to OpenAI function calling schema"""
        schemas = []
        for tool in tools:
            if callable(tool):
                schema = self._function_to_schema(tool)
            elif isinstance(tool, dict):
                schema = tool
            else:
                raise ValueError(f"Tool must be callable or dict, got {type(tool)}")
            schemas.append(schema)
        return schemas
    
    def _function_to_schema(self, func: Callable) -> Dict[str, Any]:
        """Convert a Python function to OpenAI function schema"""
        import inspect
        import json
        from typing import get_type_hints
        
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        properties = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            param_type = type_hints.get(param_name, str)
            
            # Convert Python types to JSON schema types
            if param_type == str:
                prop_type = "string"
            elif param_type == int:
                prop_type = "integer"
            elif param_type == float:
                prop_type = "number"
            elif param_type == bool:
                prop_type = "boolean"
            elif param_type == list:
                prop_type = "array"
            elif param_type == dict:
                prop_type = "object"
            else:
                prop_type = "string"  # Default fallback
            
            properties[param_name] = {"type": prop_type}
            
            # Add parameter to required if it has no default value
            if param.default == inspect.Parameter.empty:
                required.append(param_name)
        
        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": func.__doc__ or f"Function {func.__name__}",
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }
    
    def _has_bound_tools(self) -> bool:
        """Check if this service has bound tools"""
        return hasattr(self, '_bound_tools') and self._bound_tools
    
    def _get_bound_tools(self) -> List[Dict[str, Any]]:
        """Get the bound tools schema"""
        return getattr(self, '_bound_tools', [])
    
    def _execute_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool call by name with arguments"""
        # This is a placeholder - subclasses should implement actual tool execution
        raise NotImplementedError("Tool execution not implemented in base class")
    
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
