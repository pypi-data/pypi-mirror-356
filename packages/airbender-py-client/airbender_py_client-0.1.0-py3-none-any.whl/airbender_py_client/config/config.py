"""Configuration management for Airbender."""

import os
import re
from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field


def validate_url(url: str) -> bool:
    """Validate URL format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def get_api_base_url() -> str:
    """Get API base URL from environment."""
    url = os.getenv("AIRBENDER_API_BASE_URL", "").strip()
    if not url:
        raise ValueError(
            "AIRBENDER_API_BASE_URL environment variable is required. "
            "Please set it to your Airbender dashboard API URL (e.g., https://app.airbender.io/api/v1)"
        )

    if not validate_url(url):
        raise ValueError(f"Invalid AIRBENDER_API_BASE_URL: {url}")

    return url.rstrip("/")


class AirbenderConfig(BaseModel):
    """Configuration for Airbender client."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    product_key: str = Field(..., min_length=1)
    api_base_url: str = Field(default_factory=get_api_base_url)
    log_inputs: bool = True
    log_outputs: bool = True
    should_validate_before_logging: bool = True
    timeout: float = 30.0
    max_retries: int = 3

    # Callback functions
    on_response: Callable[[Any], None] | None = None
    on_log_id: Callable[[str], None] | None = None
    on_error: Callable[[Exception], None] | None = None

    def model_post_init(self, __context: Any) -> None:
        """Validate configuration after initialization."""
        if not validate_url(self.api_base_url):
            raise ValueError(f"Invalid api_base_url: {self.api_base_url}")

        if not re.match(r"^[a-zA-Z0-9\-_]+$", self.product_key):
            raise ValueError(
                "product_key must contain only alphanumeric characters, hyphens, and underscores"
            )
