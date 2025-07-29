"""Base models for Airbender Python client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from .message import ChatMessages


class BaseInput(BaseModel):
    """Standard LLM input parameters."""

    model_config = ConfigDict(populate_by_name=True)

    prompt: str | None = None
    messages: list[dict[str, Any]] | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(None, alias="maxTokens", gt=0)
    top_p: float | None = Field(None, alias="topP", ge=0.0, le=1.0)
    frequency_penalty: float | None = Field(None, alias="frequencyPenalty", ge=-2.0, le=2.0)
    presence_penalty: float | None = Field(None, alias="presencePenalty", ge=-2.0, le=2.0)
    model: str | None = None
    system: str | None = None


class UserInfo(BaseModel):
    """User information for session tracking."""

    id: str | None = None
    email: str | None = None
    name: str | None = None
    metadata: dict[str, Any] | None = None


class SendFeedbackProps(BaseModel):
    """Properties for sending feedback."""

    model_config = ConfigDict(populate_by_name=True)

    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None
    update_id: str = Field(..., alias="updateId")
    session_id: str | None = Field(None, alias="sessionId")
    item_id: str | None = Field(None, alias="itemId")


class FeedbackResponse(BaseModel):
    """Response from feedback submission."""

    model_config = ConfigDict(populate_by_name=True)

    feedback: str | None = None
    update_id: str = Field(..., alias="updateId")
    success: bool = True
    error: str | None = None


@runtime_checkable
class ProviderProtocol(Protocol):
    """Protocol that all Airbender providers must implement."""

    def supported_models(self) -> list[str]:
        """Return list of supported models for this provider."""
        ...

    async def generate_text(
        self, model: str, messages: ChatMessages | list[dict[str, Any]], **kwargs: Any
    ) -> Any:
        """Generate text using this provider."""
        ...

    async def stream_text(
        self, model: str, messages: ChatMessages | list[dict[str, Any]], **kwargs: Any
    ) -> Any:
        """Stream text using this provider."""
        ...


# Provider format: Provider name -> provider instance
Provider = dict[str, ProviderProtocol]


class ModelReference(BaseModel):
    """Reference to a specific model and provider."""

    model_config = ConfigDict(populate_by_name=True)

    provider: str
    model_id: str = Field(..., alias="modelId")
