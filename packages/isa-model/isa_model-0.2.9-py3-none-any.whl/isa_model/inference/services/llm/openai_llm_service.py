import logging
import os
import json
from typing import Dict, Any, List, Union, AsyncGenerator, Optional, Callable

# 使用官方 OpenAI 库和 dotenv
from openai import AsyncOpenAI
from dotenv import load_dotenv

from isa_model.inference.services.llm.base_llm_service import BaseLLMService
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
        self.total_token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "requests_count": 0}
        
        # Tool binding attributes
        self._bound_tools: List[Dict[str, Any]] = []
        self._tool_binding_kwargs: Dict[str, Any] = {}
        self._tool_functions: Dict[str, Callable] = {}
        
        logger.info(f"Initialized OpenAILLMService with model {self.model_name} and endpoint {self.client.base_url}")
    
    def _create_bound_copy(self) -> 'OpenAILLMService':
        """Create a copy of this service for tool binding"""
        bound_service = OpenAILLMService(self.provider, self.model_name)
        bound_service._bound_tools = self._bound_tools.copy()
        bound_service._tool_binding_kwargs = self._tool_binding_kwargs.copy()
        bound_service._tool_functions = self._tool_functions.copy()
        return bound_service
    
    def bind_tools(self, tools: List[Union[Dict[str, Any], Callable]], **kwargs) -> 'OpenAILLMService':
        """Bind tools to this LLM service for function calling"""
        bound_service = self._create_bound_copy()
        bound_service._bound_tools = self._convert_tools_to_schema(tools)
        bound_service._tool_binding_kwargs = kwargs
        
        # Store the actual functions for execution
        for tool in tools:
            if callable(tool):
                bound_service._tool_functions[tool.__name__] = tool
        
        return bound_service
    
    async def ainvoke(self, prompt: Union[str, List[Any], Any]) -> str:
        """Universal invocation method"""
        if isinstance(prompt, str):
            return await self.acompletion(prompt)
        elif isinstance(prompt, list):
            if not prompt:
                raise ValueError("Empty message list provided")
            
            # 检查是否是 LangGraph 消息对象
            first_msg = prompt[0]
            if hasattr(first_msg, 'content') and hasattr(first_msg, 'type'):
                # 转换 LangGraph 消息对象为标准格式
                converted_messages = []
                for msg in prompt:
                    if hasattr(msg, 'type') and hasattr(msg, 'content'):
                        # LangGraph 消息对象
                        msg_dict = {"content": msg.content}
                        
                        # 根据消息类型设置 role
                        if msg.type == "system":
                            msg_dict["role"] = "system"
                        elif msg.type == "human":
                            msg_dict["role"] = "user"
                        elif msg.type == "ai":
                            msg_dict["role"] = "assistant"
                            # 处理工具调用
                            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                                msg_dict["tool_calls"] = [
                                    {
                                        "id": tc.get("id", f"call_{i}"),
                                        "type": "function",
                                        "function": {
                                            "name": tc["name"],
                                            "arguments": json.dumps(tc["args"])
                                        }
                                    } for i, tc in enumerate(msg.tool_calls)
                                ]
                        elif msg.type == "tool":
                            msg_dict["role"] = "tool"
                            if hasattr(msg, 'tool_call_id'):
                                msg_dict["tool_call_id"] = msg.tool_call_id
                        else:
                            msg_dict["role"] = "user"  # 默认为用户消息
                        
                        converted_messages.append(msg_dict)
                    elif isinstance(msg, dict):
                        # 已经是字典格式
                        converted_messages.append(msg)
                    else:
                        # 处理其他类型（如字符串）
                        converted_messages.append({"role": "user", "content": str(msg)})
                
                return await self.achat(converted_messages)
            elif isinstance(first_msg, dict):
                # 标准字典格式的消息
                return await self.achat(prompt)
            else:
                # 处理其他格式，如字符串列表
                converted_messages = []
                for msg in prompt:
                    if isinstance(msg, str):
                        converted_messages.append({"role": "user", "content": msg})
                    elif isinstance(msg, dict):
                        converted_messages.append(msg)
                    else:
                        converted_messages.append({"role": "user", "content": str(msg)})
                return await self.achat(converted_messages)
        else:
            raise ValueError("Prompt must be a string or a list of messages")
    
    async def achat(self, messages: List[Dict[str, str]]) -> str:
        """Chat completion method"""
        try:
            temperature = self.config.get("temperature", 0.7)
            max_tokens = self.config.get("max_tokens", 1024)
            
            kwargs = {
                "model": self.model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            # Add tools if bound
            if self._has_bound_tools():
                kwargs["tools"] = self._get_bound_tools()
                kwargs["tool_choice"] = "auto"
            
            response = await self.client.chat.completions.create(**kwargs)
            
            if response.usage:
                self.last_token_usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
                
                # Update total usage
                self.total_token_usage["prompt_tokens"] += self.last_token_usage["prompt_tokens"]
                self.total_token_usage["completion_tokens"] += self.last_token_usage["completion_tokens"]
                self.total_token_usage["total_tokens"] += self.last_token_usage["total_tokens"]
                self.total_token_usage["requests_count"] += 1
            
            # Handle tool calls if present
            message = response.choices[0].message
            if message.tool_calls:
                return await self._handle_tool_calls(message, messages)
            
            return message.content or ""
            
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise
    
    async def _handle_tool_calls(self, assistant_message, original_messages: List[Dict[str, str]]) -> str:
        """Handle tool calls from the assistant"""
        # Add assistant message with tool calls to conversation
        messages = original_messages + [{
            "role": "assistant", 
            "content": assistant_message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in assistant_message.tool_calls
            ]
        }]
        
        # Execute each tool call
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            try:
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
                    "tool_call_id": tool_call.id
                })
                
            except Exception as e:
                logger.error(f"Error executing tool {function_name}: {e}")
                messages.append({
                    "role": "tool",
                    "content": f"Error executing {function_name}: {str(e)}",
                    "tool_call_id": tool_call.id
                })
        
        # Get final response from the model with all context
        try:
            kwargs = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.config.get("temperature", 0.7),
                "max_tokens": self.config.get("max_tokens", 1024)
            }
            
            response = await self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content or ""
            
        except Exception as e:
            logger.error(f"Error getting final response after tool calls: {e}")
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
            
            kwargs = {
                "model": self.model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "n": n
            }
            
            # Add tools if bound
            if self._has_bound_tools():
                kwargs["tools"] = self._get_bound_tools()
                kwargs["tool_choice"] = "auto"
            
            response = await self.client.chat.completions.create(**kwargs)
            
            if response.usage:
                self.last_token_usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
                
                # Update total usage
                self.total_token_usage["prompt_tokens"] += self.last_token_usage["prompt_tokens"]
                self.total_token_usage["completion_tokens"] += self.last_token_usage["completion_tokens"]
                self.total_token_usage["total_tokens"] += self.last_token_usage["total_tokens"]
                self.total_token_usage["requests_count"] += 1
            
            return [choice.message.content or "" for choice in response.choices]
        except Exception as e:
            logger.error(f"Error in generate: {e}")
            raise
    
    async def astream_chat(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        """Stream chat responses"""
        try:
            temperature = self.config.get("temperature", 0.7)
            max_tokens = self.config.get("max_tokens", 1024)
            
            kwargs = {
                "model": self.model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }
            
            # Add tools if bound
            if self._has_bound_tools():
                kwargs["tools"] = self._get_bound_tools()
                kwargs["tool_choice"] = "auto"
            
            stream = await self.client.chat.completions.create(**kwargs)
            
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
                
        except Exception as e:
            logger.error(f"Error in stream chat: {e}")
            raise
    
    async def astream_completion(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream completion responses"""
        messages = [{"role": "user", "content": prompt}]
        async for chunk in self.astream_chat(messages):
            yield chunk
    
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
            "max_tokens": self.config.get("max_tokens", 1024),
            "supports_streaming": True,
            "supports_functions": True,
            "provider": "openai"
        }
    
    def _has_bound_tools(self) -> bool:
        """Check if this service has bound tools"""
        return bool(self._bound_tools)
    
    def _get_bound_tools(self) -> List[Dict[str, Any]]:
        """Get the bound tools schema"""
        return self._bound_tools
        
    async def close(self):
        """Close the backend client"""
        await self.client.close()