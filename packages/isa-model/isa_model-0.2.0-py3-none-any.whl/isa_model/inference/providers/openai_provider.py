from isa_model.inference.providers.base_provider import BaseProvider
from isa_model.inference.base import ModelType, Capability
from typing import Dict, List, Any
import logging
import os

logger = logging.getLogger(__name__)

class OpenAIProvider(BaseProvider):
    """Provider for OpenAI API"""
    
    def __init__(self, config=None):
        """
        Initialize the OpenAI Provider
        
        Args:
            config (dict, optional): Configuration for the provider
                - api_key: OpenAI API key (can be passed here or via environment variable)
                - api_base: Base URL for OpenAI API (default: https://api.openai.com/v1)
                - timeout: Timeout for API calls in seconds
        """
        default_config = {
            "api_key": "",  # Will be set from config or environment
            "api_base": os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1"),
            "timeout": 60,
            "stream": True,
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 1024
        }
        
        # Merge default config with provided config
        merged_config = {**default_config, **(config or {})}
        
        # Set API key from config first, then fallback to environment variable
        if not merged_config["api_key"]:
            merged_config["api_key"] = os.environ.get("OPENAI_API_KEY", "")
        
        super().__init__(config=merged_config)
        self.name = "openai"
        
        logger.info(f"Initialized OpenAIProvider with URL: {self.config['api_base']}")
        
        # Only warn if no API key is provided at all
        if not self.config["api_key"]:
            logger.info("OpenAI API key not provided. You can set it via OPENAI_API_KEY environment variable or pass it in the config when creating services.")
    
    def set_api_key(self, api_key: str):
        """
        Set the API key after initialization
        
        Args:
            api_key: OpenAI API key
        """
        self.config["api_key"] = api_key
        logger.info("OpenAI API key updated")
    
    def get_capabilities(self) -> Dict[ModelType, List[Capability]]:
        """Get provider capabilities by model type"""
        return {
            ModelType.LLM: [
                Capability.CHAT, 
                Capability.COMPLETION
            ],
            ModelType.EMBEDDING: [
                Capability.EMBEDDING
            ],
            ModelType.VISION: [
                Capability.IMAGE_GENERATION,
                Capability.MULTIMODAL_UNDERSTANDING
            ],
            ModelType.AUDIO: [
                Capability.SPEECH_TO_TEXT
            ]
        }
    
    def get_models(self, model_type: ModelType) -> List[str]:
        """Get available models for given type"""
        if model_type == ModelType.LLM:
            return ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
        elif model_type == ModelType.EMBEDDING:
            return ["text-embedding-3-large", "text-embedding-3-small", "text-embedding-ada-002"]
        elif model_type == ModelType.VISION:
            return ["gpt-4o", "gpt-4-vision-preview"]
        elif model_type == ModelType.AUDIO:
            return ["whisper-1"]
        else:
            return []
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        # Return a copy without sensitive information
        config_copy = self.config.copy()
        if "api_key" in config_copy:
            config_copy["api_key"] = "***" if config_copy["api_key"] else ""
        return config_copy
    
    def is_reasoning_model(self, model_name: str) -> bool:
        """Check if the model is optimized for reasoning tasks"""
        reasoning_models = ["gpt-4", "gpt-4o", "gpt-4-turbo"]
        return any(rm in model_name.lower() for rm in reasoning_models) 