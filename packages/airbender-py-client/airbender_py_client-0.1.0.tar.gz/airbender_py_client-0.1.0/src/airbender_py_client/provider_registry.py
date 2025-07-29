"""Provider registry and loading system for Airbender client."""

import logging
from typing import Any

from .models import ChatMessage, ChatMessages, ModelReference, Provider, ProviderProtocol

logger = logging.getLogger(__name__)


class ProviderRegistry:
    """Registry for managing AI providers in Airbender client."""

    def __init__(self, providers: Provider):
        """Initialize provider registry."""
        self.providers = providers

    def get_supported_models(self, provider_name: str) -> list[str]:
        """Get supported models for a provider."""
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not found")

        provider = self.providers[provider_name]
        return provider.supported_models()

    def get_provider_instance(self, provider_name: str) -> ProviderProtocol:
        """Get provider instance."""
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not found")

        return self.providers[provider_name]

    def validate_model_reference(self, model_ref: ModelReference) -> bool:
        """Validate that a model reference is supported."""
        try:
            supported_models = self.get_supported_models(model_ref.provider)
            return model_ref.model_id in supported_models
        except ValueError:
            return False

    def list_providers(self) -> list[str]:
        """List all available provider names."""
        return list(self.providers.keys())

    def list_all_models(self) -> dict[str, list[str]]:
        """List all models grouped by provider."""
        return {
            provider_name: self.get_supported_models(provider_name)
            for provider_name in self.list_providers()
        }

    async def generate_text_with_provider(
        self,
        model_ref: ModelReference,
        messages: ChatMessages | list[dict[str, Any]],
        **kwargs: Any,
    ) -> Any:
        """Generate text using a specific provider."""
        # Validate model reference
        if not self.validate_model_reference(model_ref):
            raise ValueError(
                f"Model '{model_ref.model_id}' not supported by provider '{model_ref.provider}'"
            )

        # Convert messages to provider format if needed
        provider_messages = self._prepare_messages(messages, model_ref.provider)

        # Get provider instance and generate text
        provider = self.get_provider_instance(model_ref.provider)
        return await provider.generate_text(
            model=model_ref.model_id, messages=provider_messages, **kwargs
        )

    async def stream_text_with_provider(
        self,
        model_ref: ModelReference,
        messages: ChatMessages | list[dict[str, Any]],
        **kwargs: Any,
    ) -> Any:
        """Stream text using a specific provider."""
        # Validate model reference
        if not self.validate_model_reference(model_ref):
            raise ValueError(
                f"Model '{model_ref.model_id}' not supported by provider '{model_ref.provider}'"
            )

        # Convert messages to provider format if needed
        provider_messages = self._prepare_messages(messages, model_ref.provider)

        # Get provider instance and stream text
        provider = self.get_provider_instance(model_ref.provider)
        return await provider.stream_text(
            model=model_ref.model_id, messages=provider_messages, **kwargs
        )

    def find_provider_for_model(self, model_id: str) -> str | None:
        """Find which provider supports a given model."""
        for provider_name in self.list_providers():
            supported_models = self.get_supported_models(provider_name)
            if model_id in supported_models:
                return provider_name
        return None

    def auto_select_model_reference(
        self, model_id: str, preferred_provider: str | None = None
    ) -> ModelReference:
        """Auto-select a model reference, optionally preferring a specific provider."""
        if preferred_provider and preferred_provider in self.providers:
            supported_models = self.get_supported_models(preferred_provider)
            if model_id in supported_models:
                return ModelReference(provider=preferred_provider, model_id=model_id)  # type: ignore[call-arg]

        # Fall back to finding any provider that supports this model
        provider_name = self.find_provider_for_model(model_id)
        if not provider_name:
            raise ValueError(
                f"Model '{model_id}' not supported by any registered provider. "
                f"Available models: {self.list_all_models()}"
            )

        return ModelReference(provider=provider_name, model_id=model_id)  # type: ignore[call-arg]

    def _prepare_messages(
        self, messages: ChatMessages | list[dict[str, Any]], provider: str
    ) -> list[dict[str, Any]]:
        """Convert messages to provider-specific format."""
        if isinstance(messages, list) and all(isinstance(m, ChatMessage) for m in messages):
            # Convert ChatMessage instances to provider format
            return [msg.to_provider_format(provider) for msg in messages]
        elif isinstance(messages, list) and all(isinstance(m, dict) for m in messages):
            # Legacy support: validate and pass through dictionaries
            # Could optionally convert to ChatMessage for validation
            return messages
        else:
            raise TypeError("Messages must be a list of ChatMessage instances or dictionaries")
