# Airbender Python Client Library

The core Python SDK for integrating AI applications with Airbender's real-time governance and monitoring platform.

## Overview

The Airbender Python client provides comprehensive instrumentation for LLM calls, enabling real-time monitoring, session management, and feedback collection. It supports multiple AI providers through a unified interface while maintaining detailed logs in the Airbender dashboard.

## Features

- **Multi-Provider Support**: Unified API across OpenAI, Anthropic, and Google AI
- **Session Management**: Track related LLM interactions across multiple calls
- **Feedback Collection**: Built-in user rating and comment system
- **Event Logging**: Detailed activity tracking for governance and analytics
- **Async-First Design**: Built for high-performance applications with async/await
- **Type Safety**: Comprehensive Pydantic models with strict validation
- **Error Handling**: Robust retry logic and graceful degradation

## Installation

```bash
# Core client library
pip install airbender-py-client

# Provider plugins (install as needed)
pip install airbender-py-openai      # For OpenAI models
pip install airbender-py-anthropic   # For Claude models
pip install airbender-py-google      # For Gemini models
```

## Quick Start

### Basic Setup

```python
from airbender_py_client import create_airbender
from airbender_py_openai import init as openai_init
from airbender_py_anthropic import init as anthropic_init
from airbender_py_google import init as google_init

# Initialize client with providers
client = await create_airbender(
    product_key="your-product-key",
    api_base_url="https://your-dashboard.com/api/v1",
    providers={
        "openai": openai_init(api_key="sk-..."),
        "anthropic": anthropic_init(api_key="sk-ant-..."),
        "google": google_init(api_key="...")
    }
)

# Generate text using any provider
response = await client.generate_text(
    airbender_agent="chat-interaction",
    model="gpt-4o",  # Automatically selects OpenAI provider
    messages=[{"role": "user", "content": "Hello, world!"}],
    temperature=0.7
)

print(response.text)  # AI-generated response
print(response.usage.total_tokens)  # Token usage information

# Submit user feedback
await client.send_feedback(
    rating=5,
    comment="Great response!",
    log_id=response.log_id
)
```

### Environment Configuration

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Required environment variables
AIRBENDER_API_BASE_URL = os.getenv("AIRBENDER_API_BASE_URL")
AIRBENDER_PRODUCT_KEY = os.getenv("AIRBENDER_PRODUCT_KEY")

# Provider API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
```

## Core Concepts

### Sessions

Sessions group related LLM interactions, enabling context tracking and conversation management.

```python
# Create a new session
client = await create_airbender(
    product_key="your-product-key",
    providers={...}
)

# Resume an existing session
client = await resume_airbender(
    session_id="existing-session-id",
    product_key="your-product-key",
    providers={...}
)

# Access session information
print(client.session.session_id)
print(client.session.product_key)
```

### Unified Message Interface

The `ChatMessage` class provides a unified interface that works across all providers, automatically handling format conversion:

```python
from airbender_py_client.models import ChatMessage

# Create messages using the unified interface
messages = [
    ChatMessage(role="system", content="You are a helpful assistant."),
    ChatMessage(role="user", content="Hello, how are you?"),
    ChatMessage(role="assistant", content="I'm doing well, thank you!")
]

# Works with any provider - automatic format conversion
response = await client.generate_text(
    airbender_agent="chat",
    model="gpt-4o",  # OpenAI format
    messages=messages
)

response = await client.generate_text(
    airbender_agent="chat",
    model="claude-3-haiku-20240307",  # Converts to Anthropic format
    messages=messages
)

response = await client.generate_text(
    airbender_agent="chat",
    model="gemini-1.5-flash-8b",  # Converts to Google format
    messages=messages
)
```

**Message Format Conversion:**

- **OpenAI**: `role: "user|assistant|system"` (native format)
- **Anthropic**: `role: "human|assistant|system"` (user → human)
- **Google**: `role: "user|model|system"` (assistant → model)

**Legacy Support:**

```python
# Also supports raw dictionaries (for backward compatibility)
messages = [
    {"role": "user", "content": "Hello"}
]
```

### Providers & Auto-Fallback

Providers handle AI model integration through a consistent interface with automatic provider selection and fallback capabilities:

```python
# Automatic provider selection by model name
response = await client.generate_text(
    airbender_agent="assistant",
    model="gpt-4o",  # Automatically selects OpenAI provider
    messages=[{"role": "user", "content": "Hello"}]
)

response = await client.generate_text(
    airbender_agent="assistant",
    model="claude-3-haiku-20240307",  # Automatically selects Anthropic provider
    messages=[{"role": "user", "content": "Hello"}]
)

# Explicit provider selection
from airbender_py_client.models import ModelReference

response = await client.generate_text(
    airbender_agent="assistant",
    model=ModelReference(provider="google", model_id="gemini-1.5-flash-8b"),
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Auto-Fallback System:**
The client automatically finds the right provider for any model and can fallback across providers:

```python
# If you have multiple providers configured
client = await create_airbender(
    product_key="your-key",
    providers={
        "openai": openai_init(api_key="sk-..."),
        "anthropic": anthropic_init(api_key="sk-ant-..."),
        "google": google_init(api_key="...")
    }
)

# Just specify the model - automatic provider selection
response = await client.generate_text(
    airbender_agent="chat",
    model="gpt-4o",  # Finds OpenAI provider automatically
    messages=messages
)

# Works even if you don't know which provider has the model
response = await client.generate_text(
    airbender_agent="chat",
    model="gemini-2.0-flash",  # Finds Google provider automatically
    messages=messages
)

# Error handling with helpful model suggestions
try:
    response = await client.generate_text(
        airbender_agent="chat",
        model="unknown-model",
        messages=messages
    )
except ValueError as e:
    # Shows available models: "Available models: {'openai': ['gpt-4o', ...], ...}"
    print(f"Model error: {e}")
```

### Supported Models

**OpenAI Provider:**

- `gpt-4o`
- `gpt-4o-mini`
- `gpt-4-turbo`

**Anthropic Provider:**

- `claude-3-haiku-20240307`
- `claude-3-7-sonnet-20250219`

**Google Provider:**

- `gemini-1.5-flash-8b`
- `gemini-1.5-pro-latest`
- `gemini-2.0-flash`
- `gemini-2.0-flash-lite`

## API Reference

### AirbenderClient

The main client class for interacting with AI providers.

#### `generate_text()`

Generate text using any configured provider.

```python
async def generate_text(
    self,
    airbender_agent: str,
    model: Union[str, ModelReference],
    messages: List[Dict[str, str]],
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    **kwargs
) -> TextGenerationResponse
```

**Parameters:**

- `airbender_agent`: Identifier for the AI agent/use case
- `model`: Model name (string) or ModelReference for explicit provider selection
- `messages`: List of conversation messages in OpenAI format
- `temperature`: Sampling temperature (0.0-2.0)
- `max_tokens`: Maximum tokens to generate
- `**kwargs`: Additional model-specific parameters

**Returns:**

- `TextGenerationResponse` with generated text, usage stats, and metadata

#### `send_feedback()`

Submit user feedback for a generated response.

```python
async def send_feedback(
    self,
    rating: int,
    comment: Optional[str] = None,
    log_id: Optional[str] = None,
    update_id: Optional[str] = None
) -> None
```

**Parameters:**

- `rating`: User rating (1-5 scale)
- `comment`: Optional feedback comment
- `log_id`: Log entry ID to associate feedback with
- `update_id`: Alternative update ID for feedback association

### Factory Functions

#### `create_airbender()`

Create a new Airbender client with a fresh session.

```python
async def create_airbender(
    product_key: str,
    api_base_url: Optional[str] = None,
    providers: Optional[Dict[str, Any]] = None,
    session_config: Optional[Dict[str, Any]] = None
) -> AirbenderClient
```

#### `resume_airbender()`

Resume an existing session with a known session ID.

```python
async def resume_airbender(
    session_id: str,
    product_key: str,
    api_base_url: Optional[str] = None,
    providers: Optional[Dict[str, Any]] = None
) -> AirbenderClient
```

### Data Models

#### `ChatMessage`

Universal chat message format that works across all providers.

```python
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "model", "function", "tool"]
    content: str | list[dict[str, Any]]  # String or structured content
    name: str | None = None              # For function/tool messages
    function_call: dict[str, Any] | None = None
    tool_calls: list[dict[str, Any]] | None = None

    def to_provider_format(self, provider: str) -> dict[str, Any]:
        """Convert to provider-specific format."""
        # Handles role conversion: user↔human, assistant↔model

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ChatMessage":
        """Create from dictionary with validation."""
```

**Example usage:**

```python
from airbender_py_client.models import ChatMessage

# Create messages that work with any provider
messages = [
    ChatMessage(role="system", content="You are a helpful assistant."),
    ChatMessage(role="user", content="What's the weather like?"),
    ChatMessage(
        role="assistant",
        content="I'd need your location to check the weather."
    )
]

# Automatically converts to provider format
response = await client.generate_text(
    airbender_agent="weather-bot",
    model="gpt-4o",  # OpenAI: roles stay as-is
    messages=messages
)

response = await client.generate_text(
    airbender_agent="weather-bot",
    model="claude-3-haiku-20240307",  # Anthropic: user→human, assistant→assistant
    messages=messages
)

response = await client.generate_text(
    airbender_agent="weather-bot",
    model="gemini-1.5-flash-8b",  # Google: assistant→model
    messages=messages
)
```

#### `TextGenerationResponse`

Response from text generation operations.

```python
@dataclass
class TextGenerationResponse:
    text: str                    # Generated text content
    log_id: str                 # Airbender log entry ID
    update_id: str              # Update identifier for feedback
    usage: UsageStats           # Token usage statistics
    provider: str               # Provider that handled the request
    model: str                  # Model used for generation
    finish_reason: Optional[str] # Generation stop reason
```

#### `UsageStats`

Token usage information.

```python
@dataclass
class UsageStats:
    prompt_tokens: int          # Tokens in the input
    completion_tokens: int      # Tokens in the output
    total_tokens: int          # Total tokens used
```

#### `SessionInfo`

Session metadata and state.

```python
@dataclass
class SessionInfo:
    session_id: str            # Unique session identifier
    product_key: str           # Associated product key
    created_at: datetime       # Session creation timestamp
    metadata: Dict[str, Any]   # Additional session data
```

## Configuration

### Environment Variables

```bash
# Required
AIRBENDER_API_BASE_URL=https://your-dashboard.com/api/v1
AIRBENDER_PRODUCT_KEY=your-product-key

# Provider API Keys (as needed)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Optional
AIRBENDER_MAX_RETRIES=3
AIRBENDER_TIMEOUT=30
```

### Programmatic Configuration

```python
client = await create_airbender(
    product_key=config.product_key,
    api_base_url=config.api_base_url,
    providers={...}
    # Add any other config options here
    max_retries=3,
    timeout=30.0,
    debug=True
)
```

## Advanced Usage

### Session Management

```python
# Create client with session metadata
client = await create_airbender(
    product_key="your-product-key",
    providers={...},
    session_config={
        "user_id": "user123",
        "conversation_type": "support_chat",
        "metadata": {"channel": "web", "version": "1.0"}
    }
)

# Access session information
session = client.session
print(f"Session ID: {session.session_id}")
print(f"Created: {session.created_at}")
```

### Concurrent Operations

```python
import asyncio

# Generate multiple responses concurrently
tasks = [
    client.generate_text(
        airbender_agent="summarizer",
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize: {doc}"}]
    )
    for doc in documents
]

responses = await asyncio.gather(*tasks)

# Process results
for i, response in enumerate(responses):
    print(f"Summary {i+1}: {response.text}")
    print(f"Tokens used: {response.usage.total_tokens}")
```

## Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/your-org/airbender.git
cd airbender

# Install dependencies with uv
uv sync

# Run tests
uv run pytest libs/airbender-py/client/tests/

# Build package
uv build libs/airbender-py/client/
```

## Architecture

### Design Principles

1. **Async-First**: All I/O operations use async/await for optimal performance
2. **Type Safety**: Comprehensive Pydantic models with strict validation
3. **Error Resilience**: Exponential backoff retry logic with circuit breaking
4. **Provider Abstraction**: Unified interface across different AI providers
5. **Observability**: Detailed logging and metrics for monitoring
6. **Testability**: Comprehensive test coverage with mocked dependencies

## Integration Examples

### Streamlit Application

```python
import streamlit as st
from airbender_py_client import create_airbender
from airbender_py_openai import init as openai_init

@st.cache_resource
def get_client():
    return asyncio.run(create_airbender(
        product_key=st.secrets["AIRBENDER_PRODUCT_KEY"],
        providers={"openai": openai_init(api_key=st.secrets["OPENAI_API_KEY"])}
    ))

# UI
st.title("AI Chat Assistant")
user_input = st.text_input("Enter your message:")

if st.button("Send") and user_input:
    client = get_client()

    with st.spinner("Generating response..."):
        response = asyncio.run(client.generate_text(
            airbender_agent="streamlit-chat",
            model="gpt-4o",
            messages=[{"role": "user", "content": user_input}]
        ))

    st.write(response.text)

    # Feedback
    rating = st.selectbox("Rate this response:", [5, 4, 3, 2, 1])
    if st.button("Submit Feedback"):
        asyncio.run(client.send_feedback(rating=rating, log_id=response.log_id))
        st.success("Feedback submitted!")
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from airbender_py_client import create_airbender
from airbender_py_openai import init as openai_init

app = FastAPI()

# Initialize client at startup
@app.on_event("startup")
async def startup():
    app.state.airbender = await create_airbender(
        product_key="your-product-key",
        providers={"openai": openai_init(api_key="sk-...")}
    )

@app.post("/chat")
async def chat_endpoint(message: str):
    try:
        response = await app.state.airbender.generate_text(
            airbender_agent="api-chat",
            model="gpt-4o",
            messages=[{"role": "user", "content": message}]
        )
        return {"response": response.text, "log_id": response.log_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def feedback_endpoint(log_id: str, rating: int, comment: str = None):
    await app.state.airbender.send_feedback(
        rating=rating,
        comment=comment,
        log_id=log_id
    )
    return {"status": "success"}
```

## Troubleshooting

### Common Issues

**Authentication Errors:**

```python
# Verify product key is correct
client = await create_airbender(product_key="verify-this-key")

# Check API base URL
client = await create_airbender(
    product_key="key",
    api_base_url="https://correct-dashboard-url.com/api/v1"
)
```

**Provider Errors:**

```python
# Verify provider API keys
from airbender_py_openai import init as openai_init

try:
    provider = openai_init(api_key="sk-verify-this-key")
except Exception as e:
    print(f"Provider initialization failed: {e}")
```

**Network Issues:**

```python
# Increase timeouts for slow networks
from airbender_py_client.config import AirbenderConfig

config = AirbenderConfig(timeout=60.0, max_retries=5)
```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Or use environment variable
import os
os.environ["AIRBENDER_DEBUG"] = "1"
```

## Contributing

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-org/airbender.git
cd airbender

# Install Python plugin for Nx
npm install -D @nxlv/python

# Sync Python dependencies
npx nx run airbender-py-client:sync

# Run tests
npx nx run airbender-py-client:test

# Run linting
npx nx run airbender-py-client:lint
```

### Code Style

The project uses Ruff for linting and formatting:

```bash
# Lint code
npx nx run airbender-py-client:lint

# Format code
ruff format libs/airbender-py/client/src/
```

### Testing Guidelines

- Write comprehensive tests for all public methods
- Use pytest fixtures for common test setup
- Mock external dependencies with pytest-httpx
- Aim for >90% test coverage

## Resources

- [Airbender Dashboard Documentation](../../apps/airbender/dashboard/README.md)
- [Provider Libraries Documentation](../openai/README.md)
- [Python Demo Application](../../apps/client-demo-py/README.md)
- [API Reference](https://docs.airbender.dev/api)

## Support

For issues and questions:

1. Check the [troubleshooting guide](#troubleshooting)
2. Review [GitHub Issues](https://github.com/your-org/airbender/issues)
3. Join the [community Discord](https://discord.gg/airbender)
4. Contact support at support@airbender.dev

## License

Licensed under the Apache License 2.0. See [LICENSE](../../../LICENSE) for details.
