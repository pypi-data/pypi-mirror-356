"""Airbender Python Client SDK.

A Python SDK for integrating with the Airbender AI governance and monitoring platform.
"""

from .client import AirbenderClient, create_airbender, resume_airbender
from .config import AirbenderConfig, get_api_base_url
from .http import AirbenderHTTPClient
from .models import (
    BaseInput,
    ChatMessage,
    ChatMessages,
    FeedbackResponse,
    Provider,
    Role,
    SendFeedbackProps,
    SessionAPIResponse,
    SessionState,
    UserInfo,
)

__version__ = "0.1.0"

__all__ = [
    # Main client
    "AirbenderClient",
    "create_airbender",
    "resume_airbender",
    # Configuration
    "AirbenderConfig",
    "get_api_base_url",
    # HTTP client
    "AirbenderHTTPClient",
    # Models
    "BaseInput",
    "ChatMessage",
    "ChatMessages",
    "FeedbackResponse",
    "Provider",
    "Role",
    "SendFeedbackProps",
    "SessionAPIResponse",
    "SessionState",
    "UserInfo",
    # Version
    "__version__",
]
