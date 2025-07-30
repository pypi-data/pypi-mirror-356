import logging
import httpx
import json
from typing import Dict, Any, List, Union, AsyncGenerator, Optional, Callable
from isa_model.inference.services.llm.base_llm_service import BaseLLMService
from isa_model.inference.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)

class OllamaLLMService(BaseLLMService):
    """Ollama LLM service using HTTP client"""
    
    def __init__(self, provider: 'BaseProvider', model_name: str = "llama3.1"):
        super().__init__(provider, model_name)
        
        # Create HTTP client for Ollama API
        base_url = self.config.get("base_url", "http://localhost:11434")
        timeout = self.config.get("timeout", 60)
        
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout
        )
            
        self.last_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        self.total_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "requests_count": 0}
        
        # Tool binding attributes
        self._bound_tools: List[Dict[str, Any]] = []
        self._tool_binding_kwargs: Dict[str, Any] = {}
        self._tool_functions: Dict[str, Callable] = {}
        
        logger.info(f"Initialized OllamaLLMService with model {model_name} at {base_url}")
    
    def _create_bound_copy(self) -> 'OllamaLLMService':
        """Create a copy of this service for tool binding"""
        bound_service = OllamaLLMService(self.provider, self.model_name)
        bound_service._bound_tools = self._bound_tools.copy()
        bound_service._tool_binding_kwargs = self._tool_binding_kwargs.copy()
        bound_service._tool_functions = self._tool_functions.copy()
        return bound_service
    
    def bind_tools(self, tools: List[Union[Dict[str, Any], Callable]], **kwargs) -> 'OllamaLLMService':
        """Bind tools to this LLM service for function calling"""
        bound_service = self._create_bound_copy()
        bound_service._bound_tools = self._convert_tools_to_schema(tools)
        bound_service._tool_binding_kwargs = kwargs
        
        # Store the actual functions for execution
        for tool in tools:
            if callable(tool):
                bound_service._tool_functions[tool.__name__] = tool
        
        return bound_service
    
    async def ainvoke(self, prompt: Union[str, List[Dict[str, str]], Any]):
        """Universal invocation method"""
        if isinstance(prompt, str):
            return await self.acompletion(prompt)
        elif isinstance(prompt, list):
            return await self.achat(prompt)
        else:
            raise ValueError("Prompt must be string or list of messages")
    
    async def achat(self, messages: List[Dict[str, str]]):
        """Chat completion method"""
        try:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": self.config.get("temperature", 0.7),
                    "top_p": self.config.get("top_p", 0.9),
                    "num_predict": self.config.get("max_tokens", 2048)
                }
            }
            
            # Add tools if bound
            if self._has_bound_tools():
                payload["tools"] = self._get_bound_tools()
            
            response = await self.client.post("/api/chat", json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Update token usage if available
            if "eval_count" in result:
                self.last_token_usage = {
                    "prompt_tokens": result.get("prompt_eval_count", 0),
                    "completion_tokens": result.get("eval_count", 0),
                    "total_tokens": result.get("prompt_eval_count", 0) + result.get("eval_count", 0)
                }
                
                # Update total usage
                self.total_token_usage["prompt_tokens"] += self.last_token_usage["prompt_tokens"]
                self.total_token_usage["completion_tokens"] += self.last_token_usage["completion_tokens"]
                self.total_token_usage["total_tokens"] += self.last_token_usage["total_tokens"]
                self.total_token_usage["requests_count"] += 1
            
            # Handle tool calls if present
            message = result["message"]
            if "tool_calls" in message and message["tool_calls"]:
                return await self._handle_tool_calls(message, messages)
            
            return message["content"]
            
        except httpx.RequestError as e:
            logger.error(f"HTTP request error in chat completion: {e}")
            raise
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise
    
    async def _handle_tool_calls(self, assistant_message: Dict[str, Any], original_messages: List[Dict[str, str]]) -> str:
        """Handle tool calls from the assistant"""
        tool_calls = assistant_message.get("tool_calls", [])
        
        # Add assistant message with tool calls to conversation
        messages = original_messages + [assistant_message]
        
        # Execute each tool call
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]
            
            try:
                # Parse arguments if they're a string
                if isinstance(arguments, str):
                    arguments = json.loads(arguments)
                
                # Execute the tool
                if function_name in self._tool_functions:
                    result = self._tool_functions[function_name](**arguments)
                    if hasattr(result, '__await__'):  # Handle async functions
                        result = await result
                else:
                    result = f"Error: Function {function_name} not found"
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call.get("id", function_name)
                })
                
            except Exception as e:
                logger.error(f"Error executing tool {function_name}: {e}")
                messages.append({
                    "role": "tool",
                    "content": f"Error executing {function_name}: {str(e)}",
                    "tool_call_id": tool_call.get("id", function_name)
                })
        
        # Get final response from the model
        return await self.achat(messages)
    
    async def acompletion(self, prompt: str):
        """Text completion method"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.config.get("temperature", 0.7),
                    "top_p": self.config.get("top_p", 0.9),
                    "num_predict": self.config.get("max_tokens", 2048)
                }
            }
            
            response = await self.client.post("/api/generate", json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Update token usage if available
            if "eval_count" in result:
                self.last_token_usage = {
                    "prompt_tokens": result.get("prompt_eval_count", 0),
                    "completion_tokens": result.get("eval_count", 0),
                    "total_tokens": result.get("prompt_eval_count", 0) + result.get("eval_count", 0)
                }
                
                # Update total usage
                self.total_token_usage["prompt_tokens"] += self.last_token_usage["prompt_tokens"]
                self.total_token_usage["completion_tokens"] += self.last_token_usage["completion_tokens"]
                self.total_token_usage["total_tokens"] += self.last_token_usage["total_tokens"]
                self.total_token_usage["requests_count"] += 1
            
            return result["response"]
            
        except httpx.RequestError as e:
            logger.error(f"HTTP request error in text completion: {e}")
            raise
        except Exception as e:
            logger.error(f"Error in text completion: {e}")
            raise
    
    async def agenerate(self, messages: List[Dict[str, str]], n: int = 1) -> List[str]:
        """Generate multiple completions"""
        results = []
        for _ in range(n):
            result = await self.achat(messages)
            results.append(result)
        return results
    
    async def astream_chat(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        """Stream chat responses"""
        try:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": True,
                "options": {
                    "temperature": self.config.get("temperature", 0.7),
                    "top_p": self.config.get("top_p", 0.9),
                    "num_predict": self.config.get("max_tokens", 2048)
                }
            }
            
            # Add tools if bound
            if self._has_bound_tools():
                payload["tools"] = self._get_bound_tools()
            
            async with self.client.stream("POST", "/api/chat", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            chunk = json.loads(line)
                            if "message" in chunk and "content" in chunk["message"]:
                                content = chunk["message"]["content"]
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
                            
        except httpx.RequestError as e:
            logger.error(f"HTTP request error in stream chat: {e}")
            raise
        except Exception as e:
            logger.error(f"Error in stream chat: {e}")
            raise
    
    async def astream_completion(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream completion responses"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": self.config.get("temperature", 0.7),
                    "top_p": self.config.get("top_p", 0.9),
                    "num_predict": self.config.get("max_tokens", 2048)
                }
            }
            
            async with self.client.stream("POST", "/api/generate", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            chunk = json.loads(line)
                            if "response" in chunk:
                                content = chunk["response"]
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
                            
        except httpx.RequestError as e:
            logger.error(f"HTTP request error in stream completion: {e}")
            raise
        except Exception as e:
            logger.error(f"Error in stream completion: {e}")
            raise
    
    def get_token_usage(self) -> Dict[str, Any]:
        """Get total token usage statistics"""
        return self.total_token_usage
    
    def get_last_token_usage(self) -> Dict[str, int]:
        """Get token usage from last request"""
        return self.last_token_usage
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "name": self.model_name,
            "max_tokens": self.config.get("max_tokens", 2048),
            "supports_streaming": True,
            "supports_functions": True,
            "provider": "ollama"
        }
    
    def _has_bound_tools(self) -> bool:
        """Check if this service has bound tools"""
        return bool(self._bound_tools)
    
    def _get_bound_tools(self) -> List[Dict[str, Any]]:
        """Get the bound tools schema"""
        return self._bound_tools
        
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose() 