#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simplified AI Factory for creating inference services
Uses the new service architecture with proper base classes
"""

from typing import Dict, Type, Any, Optional, Tuple, List
import logging
import os
from isa_model.inference.providers.base_provider import BaseProvider
from isa_model.inference.services.base_service import BaseService
from isa_model.inference.base import ModelType

logger = logging.getLogger(__name__)

class AIFactory:
    """
    Simplified Factory for creating AI services with proper inheritance hierarchy
    """
    
    _instance = None
    _is_initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the AI Factory."""
        if not self._is_initialized:
            self._providers: Dict[str, Type[BaseProvider]] = {}
            self._services: Dict[Tuple[str, ModelType], Type[BaseService]] = {}
            self._cached_services: Dict[str, BaseService] = {}
            self._initialize_services()
            AIFactory._is_initialized = True
    
    def _initialize_services(self):
        """Initialize available providers and services"""
        try:
            # Register Ollama services
            self._register_ollama_services()
            
            # Register OpenAI services
            self._register_openai_services()
            
            # Register Replicate services
            self._register_replicate_services()
            
            logger.info("AI Factory initialized with simplified service architecture")
            
        except Exception as e:
            logger.error(f"Error initializing services: {e}")
            logger.warning("Some services may not be available")
    
    def _register_ollama_services(self):
        """Register Ollama provider and services"""
        try:
            from isa_model.inference.providers.ollama_provider import OllamaProvider
            from isa_model.inference.services.llm.ollama_llm_service import OllamaLLMService
            from isa_model.inference.services.embedding.ollama_embed_service import OllamaEmbedService
            from isa_model.inference.services.vision.ollama_vision_service import OllamaVisionService
            
            self.register_provider('ollama', OllamaProvider)
            self.register_service('ollama', ModelType.LLM, OllamaLLMService)
            self.register_service('ollama', ModelType.EMBEDDING, OllamaEmbedService)
            self.register_service('ollama', ModelType.VISION, OllamaVisionService)
            
            logger.info("Ollama services registered successfully")
            
        except ImportError as e:
            logger.warning(f"Ollama services not available: {e}")
    
    def _register_openai_services(self):
        """Register OpenAI provider and services"""
        try:
            from isa_model.inference.providers.openai_provider import OpenAIProvider
            from isa_model.inference.services.llm.openai_llm_service import OpenAILLMService
            from isa_model.inference.services.audio.openai_tts_service import OpenAITTSService
            
            self.register_provider('openai', OpenAIProvider)
            self.register_service('openai', ModelType.LLM, OpenAILLMService)
            self.register_service('openai', ModelType.AUDIO, OpenAITTSService)
            
            logger.info("OpenAI services registered successfully")
            
        except ImportError as e:
            logger.warning(f"OpenAI services not available: {e}")
    
    def _register_replicate_services(self):
        """Register Replicate provider and services"""
        try:
            from isa_model.inference.providers.replicate_provider import ReplicateProvider
            from isa_model.inference.services.vision.replicate_image_gen_service import ReplicateImageGenService
            
            self.register_provider('replicate', ReplicateProvider)
            self.register_service('replicate', ModelType.VISION, ReplicateImageGenService)
            
            logger.info("Replicate services registered successfully")
            
        except ImportError as e:
            logger.warning(f"Replicate services not available: {e}")
    
    def register_provider(self, name: str, provider_class: Type[BaseProvider]) -> None:
        """Register an AI provider"""
        self._providers[name] = provider_class
    
    def register_service(self, provider_name: str, model_type: ModelType, 
                        service_class: Type[BaseService]) -> None:
        """Register a service type with its provider"""
        self._services[(provider_name, model_type)] = service_class
    
    def create_service(self, provider_name: str, model_type: ModelType, 
                      model_name: str, config: Optional[Dict[str, Any]] = None) -> BaseService:
        """Create a service instance"""
        try:
            cache_key = f"{provider_name}_{model_type}_{model_name}"
            
            if cache_key in self._cached_services:
                return self._cached_services[cache_key]
            
            # Get provider and service classes
            provider_class = self._providers.get(provider_name)
            service_class = self._services.get((provider_name, model_type))
            
            if not provider_class:
                raise ValueError(f"No provider registered for '{provider_name}'")
            
            if not service_class:
                raise ValueError(
                    f"No service registered for provider '{provider_name}' and model type '{model_type}'"
                )
            
            # Create provider and service
            provider = provider_class(config=config or {})
            service = service_class(provider=provider, model_name=model_name)
            
            self._cached_services[cache_key] = service
            return service
            
        except Exception as e:
            logger.error(f"Error creating service: {e}")
            raise
    
    # Convenient methods for common services
    def get_llm_service(self, model_name: str = "llama3.1", provider: str = "ollama",
                       config: Optional[Dict[str, Any]] = None) -> BaseService:
        """
        Get a LLM service instance
        
        Args:
            model_name: Name of the model to use
            provider: Provider name ('ollama', 'openai')
            config: Optional configuration dictionary
            
        Returns:
            LLM service instance
        """
        return self.create_service(provider, ModelType.LLM, model_name, config)
    
    def get_embedding_service(self, model_name: str = "bge-m3", provider: str = "ollama",
                             config: Optional[Dict[str, Any]] = None) -> BaseService:
        """
        Get an embedding service instance
        
        Args:
            model_name: Name of the model to use
            provider: Provider name ('ollama')
            config: Optional configuration dictionary
            
        Returns:
            Embedding service instance
        """
        return self.create_service(provider, ModelType.EMBEDDING, model_name, config)
    
    def get_vision_service(self, model_name: str, provider: str,
                          config: Optional[Dict[str, Any]] = None) -> BaseService:
        """
        Get a vision service instance
        
        Args:
            model_name: Name of the model to use
            provider: Provider name ('ollama', 'replicate')
            config: Optional configuration dictionary
            
        Returns:
            Vision service instance
        """
        return self.create_service(provider, ModelType.VISION, model_name, config)
    
    def get_image_generation_service(self, model_name: str, provider: str = "replicate",
                                   config: Optional[Dict[str, Any]] = None) -> BaseService:
        """
        Get an image generation service instance
        
        Args:
            model_name: Name of the model to use (e.g., "stability-ai/sdxl")
            provider: Provider name ('replicate')
            config: Optional configuration dictionary
            
        Returns:
            Image generation service instance
        """
        return self.create_service(provider, ModelType.VISION, model_name, config)
    
    def get_audio_service(self, model_name: str = "tts-1", provider: str = "openai",
                         config: Optional[Dict[str, Any]] = None) -> BaseService:
        """
        Get an audio service instance
        
        Args:
            model_name: Name of the model to use
            provider: Provider name ('openai')
            config: Optional configuration dictionary
            
        Returns:
            Audio service instance
        """
        return self.create_service(provider, ModelType.AUDIO, model_name, config)
    
    def get_available_services(self) -> Dict[str, List[str]]:
        """Get information about available services"""
        services = {}
        for (provider, model_type), service_class in self._services.items():
            if provider not in services:
                services[provider] = []
            services[provider].append(f"{model_type.value}: {service_class.__name__}")
        return services
    
    def clear_cache(self):
        """Clear the service cache"""
        self._cached_services.clear()
        logger.info("Service cache cleared")
    
    @classmethod
    def get_instance(cls) -> 'AIFactory':
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    # Alias methods for backward compatibility with tests
    def get_llm(self, model_name: str = "llama3.1", provider: str = "ollama",
                config: Optional[Dict[str, Any]] = None) -> BaseService:
        """Alias for get_llm_service"""
        return self.get_llm_service(model_name, provider, config)
    
    def get_embedding(self, model_name: str = "bge-m3", provider: str = "ollama",
                     config: Optional[Dict[str, Any]] = None) -> BaseService:
        """Alias for get_embedding_service"""
        return self.get_embedding_service(model_name, provider, config)
    
    def get_vision_model(self, model_name: str, provider: str,
                        config: Optional[Dict[str, Any]] = None) -> BaseService:
        """Alias for get_vision_service and get_image_generation_service"""
        if provider == "replicate":
            return self.get_image_generation_service(model_name, provider, config)
        else:
            return self.get_vision_service(model_name, provider, config) 