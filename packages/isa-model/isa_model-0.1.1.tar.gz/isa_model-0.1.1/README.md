# isA Model - Unified AI Model Serving Framework

A comprehensive Python framework for working with multiple AI providers and models through a unified interface. Support for OpenAI, Replicate, Ollama, and more.

## Installation

```bash
pip install isa-model
```

## Quick Start

The isa-model package supports three main usage patterns:

### 1. Pass API Keys Directly (Recommended)

This is the most flexible approach - no environment variables needed:

```python
from isa_model.inference.ai_factory import AIFactory

# Create factory instance
factory = AIFactory.get_instance()

# Use OpenAI with API key
llm = factory.get_llm(
    model_name="gpt-4o-mini", 
    provider="openai", 
    api_key="your-openai-api-key-here"
)

# Use Replicate for image generation
image_gen = factory.get_vision_model(
    model_name="stability-ai/sdxl", 
    provider="replicate", 
    api_key="your-replicate-token-here"
)
```

### 2. Use Environment Variables

Set your API keys as environment variables:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export REPLICATE_API_TOKEN="your-replicate-token"
```

Then use without passing keys:

```python
from isa_model.inference.ai_factory import AIFactory

factory = AIFactory.get_instance()

# Will automatically use OPENAI_API_KEY from environment
llm = factory.get_llm(model_name="gpt-4o-mini", provider="openai")

# Will automatically use REPLICATE_API_TOKEN from environment  
image_gen = factory.get_vision_model(model_name="stability-ai/sdxl", provider="replicate")
```

### 3. Use Local Models (No API Key Needed)

For local models like Ollama, no API keys are required:

```python
from isa_model.inference.ai_factory import AIFactory

factory = AIFactory.get_instance()

# Use local Ollama model (no API key needed)
llm = factory.get_llm(model_name="llama3.1", provider="ollama")
```

## Supported Services

### Language Models (LLM)

```python
# OpenAI models
llm = factory.get_llm("gpt-4o-mini", "openai", api_key="your-key")
llm = factory.get_llm("gpt-4o", "openai", api_key="your-key") 

# Ollama models (local)
llm = factory.get_llm("llama3.1", "ollama")
llm = factory.get_llm("codellama", "ollama")

# Replicate models
llm = factory.get_llm("meta/llama-3-70b-instruct", "replicate", api_key="your-token")
```

### Vision Models

```python
# OpenAI vision
vision = factory.get_vision_model("gpt-4o", "openai", api_key="your-key")

# Replicate image generation
image_gen = factory.get_vision_model("stability-ai/sdxl", "replicate", api_key="your-token")

# Ollama vision (local)
vision = factory.get_vision_model("llava", "ollama")
```

### Embedding Models

```python
# OpenAI embeddings
embedder = factory.get_embedding("text-embedding-3-small", "openai", {"api_key": "your-key"})

# Ollama embeddings (local)
embedder = factory.get_embedding("bge-m3", "ollama")
```

## Base Service Classes

The framework provides comprehensive base classes for implementing new AI services:

### BaseLLMService
- `ainvoke()` - Universal invocation method
- `achat()` - Chat completion with messages
- `acompletion()` - Simple text completion
- `agenerate()` - Generate multiple completions
- `astream_chat()` - Streaming chat responses
- `get_token_usage()` - Token usage statistics

### BaseVisionService  
- `analyze_image()` - Analyze and describe images
- `describe_image()` - Generate detailed descriptions
- `extract_text()` - OCR text extraction
- `detect_objects()` - Object detection
- `classify_image()` - Image classification
- `compare_images()` - Image similarity comparison

### BaseImageGenService
- `generate_image()` - Generate single image from text
- `generate_images()` - Generate multiple images
- `image_to_image()` - Transform existing images
- `get_supported_sizes()` - Get supported dimensions

### BaseEmbedService
- `create_text_embedding()` - Single text embedding
- `create_text_embeddings()` - Batch text embeddings
- `compute_similarity()` - Similarity calculation
- `find_similar_texts()` - Semantic search

### BaseSTTService (Speech-to-Text)
- `transcribe_audio()` - Audio transcription
- `transcribe_audio_batch()` - Batch transcription
- `detect_language()` - Language detection

### BaseTTSService (Text-to-Speech)
- `synthesize_speech()` - Text to speech conversion
- `synthesize_speech_to_file()` - Save speech to file
- `get_available_voices()` - List available voices

## Usage Examples

### Chat Completion

```python
import asyncio
from isa_model.inference.ai_factory import AIFactory

async def chat_example():
    factory = AIFactory.get_instance()
    llm = factory.get_llm("gpt-4o-mini", "openai", api_key="your-key")
    
    messages = [
        {"role": "user", "content": "Hello, how are you?"}
    ]
    
    response = await llm.achat(messages)
    print(response)

# Run the async function
asyncio.run(chat_example())
```

### Image Analysis

```python
import asyncio
from isa_model.inference.ai_factory import AIFactory

async def vision_example():
    factory = AIFactory.get_instance()
    vision = factory.get_vision_model("gpt-4o", "openai", api_key="your-key")
    
    result = await vision.analyze_image(
        image="path/to/your/image.jpg",
        prompt="What do you see in this image?"
    )
    
    print(result["text"])

asyncio.run(vision_example())
```

### Image Generation

```python
import asyncio
from isa_model.inference.ai_factory import AIFactory

async def image_gen_example():
    factory = AIFactory.get_instance()
    image_gen = factory.get_vision_model(
        "stability-ai/sdxl", 
        "replicate", 
        api_key="your-replicate-token"
    )
    
    result = await image_gen.generate_image(
        prompt="A beautiful sunset over mountains",
        width=1024,
        height=1024
    )
    
    # Save the generated image
    with open("generated_image.png", "wb") as f:
        f.write(result["image_data"])

asyncio.run(image_gen_example())
```

## Configuration Options

You can pass additional configuration options:

```python
# Custom configuration
config = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.9
}

llm = factory.get_llm(
    model_name="gpt-4o-mini",
    provider="openai", 
    config=config,
    api_key="your-key"
)
```

## Error Handling

The framework provides informative error messages and graceful fallbacks:

```python
try:
    llm = factory.get_llm("gpt-4o-mini", "openai", api_key="invalid-key")
    response = await llm.achat([{"role": "user", "content": "Hello"}])
except Exception as e:
    print(f"Error: {e}")
```

## Development

### Installing for Development

```bash
git clone <repository-url>
cd isA_Model
pip install -e .
```

### Running Tests

```bash
pytest tests/
```

### Building and Publishing

```bash
# Build the package
python -m build

# Upload to PyPI (requires PYPI_API_TOKEN in .env.local)
bash scripts/normal_update.sh
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to our GitHub repository.

## Support

For questions and support, please open an issue on our GitHub repository. 