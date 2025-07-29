"""Message models for chat interactions."""

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Common role types across providers
Role = Literal["system", "user", "assistant", "model", "function", "tool"]


class ChatMessage(BaseModel):
    """
    Universal chat message format that works across providers.

    Supports OpenAI, Anthropic, and Google message formats.
    """

    model_config = ConfigDict(populate_by_name=True)

    role: Role
    content: str | list[dict[str, Any]]  # String or structured content
    name: str | None = None  # For function/tool messages

    # Provider-specific fields
    function_call: dict[str, Any] | None = Field(None, alias="functionCall")
    tool_calls: list[dict[str, Any]] | None = Field(None, alias="toolCalls")

    @field_validator("role", mode="before")
    @classmethod
    def normalize_role(cls, v: str) -> str:
        """Normalize role names across providers."""
        # Anthropic uses "human" -> "user"
        if v == "human":
            return "user"
        # Google uses "model" -> "assistant" (but preserve "model" for Google)
        return v

    def to_provider_format(self, provider: str) -> dict[str, Any]:
        """Convert to provider-specific format."""
        base = {"role": self.role, "content": self.content}

        if provider == "anthropic" and self.role == "user":
            base["role"] = "human"
        elif provider == "google" and self.role == "assistant":
            base["role"] = "model"

        # Add optional fields
        if self.name:
            base["name"] = self.name
        if self.function_call:
            base["function_call"] = self.function_call
        if self.tool_calls:
            base["tool_calls"] = self.tool_calls

        return base

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ChatMessage":
        """Create from dictionary with validation."""
        return cls.model_validate(data)


# Convenience type for lists of messages
ChatMessages = list[ChatMessage]
