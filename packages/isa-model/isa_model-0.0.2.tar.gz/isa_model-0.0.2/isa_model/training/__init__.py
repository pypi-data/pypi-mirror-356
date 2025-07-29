"""
ISA Model Training Framework

This module provides unified interfaces for training various types of AI models:
- LLM training with LlamaFactory
- Image model training with Flux/LoRA
- Model evaluation and benchmarking

Usage:
    from isa_model.training import TrainingFactory
    
    # Create training factory
    factory = TrainingFactory()
    
    # Fine-tune Gemma 3:4B
    model_path = factory.finetune_llm(
        model_name="gemma:4b",
        dataset_path="path/to/data.json",
        training_type="sft"
    )
"""

from .factory import TrainingFactory, finetune_gemma
from .engine.llama_factory import (
    LlamaFactory,
    LlamaFactoryConfig,
    SFTConfig,
    RLConfig,
    DPOConfig,
    TrainingStrategy,
    DatasetFormat
)

__all__ = [
    "TrainingFactory",
    "finetune_gemma",
    "LlamaFactory", 
    "LlamaFactoryConfig",
    "SFTConfig",
    "RLConfig", 
    "DPOConfig",
    "TrainingStrategy",
    "DatasetFormat"
] 