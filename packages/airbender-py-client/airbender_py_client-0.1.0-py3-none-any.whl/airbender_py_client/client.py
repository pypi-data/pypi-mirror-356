"""Main Airbender client implementation."""

import logging
import uuid
from typing import Any

from .config import AirbenderConfig
from .http import AirbenderHTTPClient
from .models import (
    ChatMessage,
    ChatMessages,
    ModelReference,
    Provider,
    SendFeedbackProps,
    SessionAPIResponse,
    SessionState,
    UserInfo,
)
from .provider_registry import ProviderRegistry
from .store import SessionStore

logger = logging.getLogger(__name__)


class AirbenderClient:
    """Main Airbender client for Python applications."""

    def __init__(self, config: AirbenderConfig, providers: Provider):
        self.config = config
        self.providers = providers
        self._provider_registry = ProviderRegistry(providers)
        self._http_client: AirbenderHTTPClient | None = None
        self._store = SessionStore()

        # Initialize store with basic data
        self._store.product_key = config.product_key
        self._store.providers = providers
        self._store.session_state = SessionState.NOT_STARTED

    async def __aenter__(self) -> "AirbenderClient":
        """Async context manager entry."""
        self._http_client = AirbenderHTTPClient(self.config)
        await self._http_client.__aenter__()
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Async context manager exit."""
        if self._http_client:
            await self._http_client.__aexit__(exc_type, exc_val, exc_tb)

    def _ensure_http_client(self) -> AirbenderHTTPClient:
        """Ensure HTTP client is available."""
        if not self._http_client:
            raise RuntimeError(
                "HTTP client not initialized. Use async context manager or call setup()."
            )
        return self._http_client

    async def setup(self) -> None:
        """Set up the client (alternative to context manager)."""
        if not self._http_client:
            self._http_client = AirbenderHTTPClient(self.config)
            await self._http_client.__aenter__()

    async def close(self) -> None:
        """Close the client."""
        if self._http_client:
            await self._http_client.close()

    async def _ensure_session(self) -> SessionAPIResponse:
        """Ensure a session exists and return it."""
        if self._store.session_state == SessionState.SUCCESS and self._store.session_id:
            # Session already exists and is valid
            return self._store.session_data

        # Need to create a new session
        await self._fetch_session()
        return self._store.session_data

    async def _fetch_session(self) -> SessionAPIResponse:
        """Fetch or create a new session."""
        http_client = self._ensure_http_client()

        try:
            self._store.session_state = SessionState.FETCHING

            user_str = None
            if self._store.user:
                user_str = self._store.user.model_dump_json() if self._store.user else None

            session = await http_client.create_session(
                product_key=self.config.product_key,
                user=user_str,
            )

            self._store.session_id = session.id
            self._store.session_data = session
            self._store.config = session.config
            self._store.is_blocked = session.blocked
            self._store.session_state = SessionState.SUCCESS

            logger.info(f"Created new session: {session.id}")
            return session

        except Exception as e:
            self._store.session_state = SessionState.ERROR
            logger.error(f"Failed to create session: {e}")
            if self.config.on_error:
                self.config.on_error(e)
            raise

    async def fetch_session_by_id(self, session_id: str) -> SessionAPIResponse:
        """Fetch an existing session by ID."""
        http_client = self._ensure_http_client()

        try:
            self._store.session_state = SessionState.FETCHING

            session = await http_client.fetch_session(session_id)

            self._store.session_id = session.id
            self._store.session_data = session
            self._store.config = session.config
            self._store.is_blocked = session.blocked
            self._store.session_state = SessionState.SUCCESS

            logger.info(f"Fetched existing session: {session.id}")
            return session

        except Exception as e:
            self._store.session_state = SessionState.ERROR
            logger.error(f"Failed to fetch session {session_id}: {e}")
            if self.config.on_error:
                self.config.on_error(e)
            raise

    def set_user(self, user: UserInfo):
        """Set user information for the session."""
        self._store.user = user
        logger.debug(f"Set user: {user.id}")

    def get_current_session_id(self) -> str | None:
        """Get the current session ID."""
        return self._store.session_id

    def is_session_blocked(self) -> bool:
        """Check if the current session is blocked."""
        return self._store.is_blocked

    async def fetch_llm_agents(self) -> dict[str, str]:
        """Get available LLM agents from server config."""
        session = await self._ensure_session()

        if not session.config or not session.config.control_points:
            return {}

        llm_agents = {}
        for cp in session.config.control_points:
            if cp.type == "llm":
                llm_agents[cp.key] = cp.name

        return llm_agents

    async def fetch_telemetry_agents(self) -> dict[str, Any]:
        """Get telemetry control points."""
        session = await self._ensure_session()

        if not session.config or not session.config.control_points:
            return {}

        telemetry_agents = {}
        for cp in session.config.control_points:
            if cp.type == "telemetry":
                telemetry_agents[cp.key] = {
                    "name": cp.name,
                    "settings": cp.settings,
                }

        return telemetry_agents

    async def generate_text(
        self,
        airbender_agent: str,
        model: str | ModelReference,
        messages: ChatMessages | list[dict[str, Any]],
        **kwargs: Any,
    ) -> Any:
        """
        Generate text using specified agent and provider.

        Args:
            airbender_agent: The agent identifier for Airbender logging
            model: Model to use - can be string or ModelReference
            messages: Messages for chat-based generation (ChatMessage instances or dicts)
            **kwargs: Additional parameters passed to provider

        Returns:
            Provider response with tracking attributes added
        """
        session = await self._ensure_session()

        if session.blocked:
            raise RuntimeError("Session is blocked and cannot generate text")

        # Convert model to ModelReference if needed
        if isinstance(model, str):
            model_ref = self._provider_registry.auto_select_model_reference(model)
        else:
            model_ref = model

        http_client = self._ensure_http_client()
        log_id = None

        try:
            # Step 1: Generate using provider
            logger.debug(
                f"Generating text with provider {model_ref.provider}, model {model_ref.model_id}"
            )
            provider_response = await self._provider_registry.generate_text_with_provider(
                model_ref=model_ref, messages=messages, **kwargs
            )

            # Step 2: Extract response text for logging
            response_text = self._extract_response_text(provider_response, model_ref.provider)

            # Step 3: Create log entry with both input and output
            try:
                logger.debug(f"Creating log entry for agent: {airbender_agent}")

                # Normalize messages to list of dicts for logging
                if isinstance(messages, list) and all(isinstance(m, ChatMessage) for m in messages):
                    messages_for_log = [msg.model_dump(exclude_none=True) for msg in messages]
                else:
                    messages_for_log = messages

                # Prepare input data
                input_data = {
                    "messages": messages_for_log,
                    "model": model_ref.model_id,
                    "provider": model_ref.provider,
                    **kwargs,
                }

                # Serialize provider response to JSON-compatible format
                output_data = self._serialize_provider_response(
                    provider_response, model_ref.provider
                )

                # Extract system prompt from kwargs if provided
                system_prompt = kwargs.get("system", kwargs.get("system_prompt"))

                # Look up control point ID for this agent if available
                control_point_id = None
                if session.config and session.config.control_points:
                    for cp in session.config.control_points:
                        if cp.key == airbender_agent:
                            control_point_id = (
                                cp.settings.get("id")
                                if hasattr(cp, "settings") and cp.settings
                                else None
                            )
                            # If no system prompt provided, try to get it from control point
                            if not system_prompt and cp.settings:
                                system_prompt = cp.settings.get("system_prompt")
                            break

                # Create log entry
                log_response = await http_client.create_log(
                    session_id=session.id,
                    airbender_agent=airbender_agent,
                    model=model_ref.model_id,
                    provider=model_ref.provider,
                    input_data=input_data,
                    output_data=output_data,
                    dynamic_model=True,
                    system_prompt=system_prompt,
                    control_point_id=control_point_id,
                )

                log_id = log_response.get("id")
                logger.debug(f"Log entry created with id: {log_id}")

            except Exception as log_error:
                logger.warning(f"Failed to create log entry: {log_error}")
                # Continue without logging rather than failing the generation

            # Step 4: Add tracking attributes to provider response
            provider_response.update_id = log_id or str(uuid.uuid4())
            provider_response.success = True

            # Step 5: Trigger callbacks
            if self.config.on_response:
                self.config.on_response(
                    {
                        "response": response_text,
                        "updateId": provider_response.update_id,
                        "provider": model_ref.provider,
                        "model": model_ref.model_id,
                        "agent": airbender_agent,
                    }
                )

            if self.config.on_log_id:
                self.config.on_log_id(provider_response.update_id)

            logger.debug("Text generation completed successfully")
            return provider_response

        except Exception as e:
            logger.error(f"Failed to generate text: {e}")

            # Try to create an error log entry
            if not log_id:
                try:
                    # Normalize messages to list of dicts for logging
                    if isinstance(messages, list) and all(
                        isinstance(m, ChatMessage) for m in messages
                    ):
                        messages_for_log = [msg.model_dump(exclude_none=True) for msg in messages]
                    else:
                        messages_for_log = messages

                    input_data = {
                        "messages": messages_for_log,
                        "model": model_ref.model_id,
                        "provider": model_ref.provider,
                        **kwargs,
                    }

                    # Extract system prompt from kwargs for error logging too
                    system_prompt = kwargs.get("system", kwargs.get("system_prompt"))

                    # Look up control point ID for this agent if available
                    control_point_id = None
                    if session.config and session.config.control_points:
                        for cp in session.config.control_points:
                            if cp.key == airbender_agent:
                                control_point_id = (
                                    cp.settings.get("id")
                                    if hasattr(cp, "settings") and cp.settings
                                    else None
                                )
                                if not system_prompt and cp.settings:
                                    system_prompt = cp.settings.get("system_prompt")
                                break

                    await http_client.create_log(
                        session_id=session.id,
                        airbender_agent=airbender_agent,
                        model=model_ref.model_id,
                        provider=model_ref.provider,
                        input_data=input_data,
                        output_data={"error": str(e), "provider": model_ref.provider},
                        dynamic_model=True,
                        system_prompt=system_prompt,
                        control_point_id=control_point_id,
                    )
                except Exception as log_error:
                    logger.warning(f"Failed to log error: {log_error}")

            if self.config.on_error:
                self.config.on_error(e)
            raise

    def _extract_response_text(self, provider_response: Any, provider_name: str) -> str:
        """Extract response text from provider-specific response format."""
        # Handle different provider response formats
        if provider_name == "openai":
            # OpenAI format: response.choices[0].message.content
            if hasattr(provider_response, "choices") and provider_response.choices:
                return provider_response.choices[0].message.content or ""
        elif provider_name == "anthropic":
            # Anthropic format: response.content[0].text
            if hasattr(provider_response, "content") and provider_response.content:
                return provider_response.content[0].text or ""
        elif provider_name == "google":
            # Google format: response.text
            if hasattr(provider_response, "text"):
                return provider_response.text or ""

        # Generic fallback - try common attributes
        for attr in ["text", "content", "response"]:
            if hasattr(provider_response, attr):
                value = getattr(provider_response, attr)
                if isinstance(value, str):
                    return value

        # Last resort - convert to string
        return str(provider_response)

    def _serialize_provider_response(
        self, provider_response: Any, provider_name: str
    ) -> dict[str, Any]:
        """Convert provider response to JSON-serializable format."""
        try:
            # Try to convert to dict/JSON format
            if provider_name == "openai":
                # OpenAI response structure
                if hasattr(provider_response, "choices"):
                    return {
                        "text": provider_response.choices[0].message.content
                        if provider_response.choices
                        else "",
                        "choices": [
                            {
                                "message": {
                                    "role": choice.message.role,
                                    "content": choice.message.content,
                                },
                                "finish_reason": choice.finish_reason,
                                "index": choice.index,
                            }
                            for choice in provider_response.choices
                        ],
                        "usage": {
                            "prompt_tokens": getattr(provider_response.usage, "prompt_tokens", 0),
                            "completion_tokens": getattr(
                                provider_response.usage, "completion_tokens", 0
                            ),
                            "total_tokens": getattr(provider_response.usage, "total_tokens", 0),
                        }
                        if hasattr(provider_response, "usage") and provider_response.usage
                        else {},
                        "model": getattr(provider_response, "model", ""),
                        "id": getattr(provider_response, "id", ""),
                    }

            elif provider_name == "anthropic":
                # Anthropic response structure
                if hasattr(provider_response, "content"):
                    return {
                        "text": provider_response.content[0].text
                        if provider_response.content
                        else "",
                        "content": [
                            {"type": block.type, "text": block.text}
                            for block in provider_response.content
                        ],
                        "usage": {
                            "input_tokens": getattr(provider_response.usage, "input_tokens", 0),
                            "output_tokens": getattr(provider_response.usage, "output_tokens", 0),
                            "total_tokens": getattr(provider_response.usage, "input_tokens", 0)
                            + getattr(provider_response.usage, "output_tokens", 0),
                        }
                        if hasattr(provider_response, "usage") and provider_response.usage
                        else {},
                        "model": getattr(provider_response, "model", ""),
                        "id": getattr(provider_response, "id", ""),
                        "role": getattr(provider_response, "role", "assistant"),
                        "stop_reason": getattr(provider_response, "stop_reason", None),
                    }

            elif provider_name == "google":
                # Google response structure
                return {
                    "text": getattr(provider_response, "text", ""),
                    "usage": {
                        "prompt_token_count": getattr(
                            provider_response.usage_metadata, "prompt_token_count", 0
                        ),
                        "candidates_token_count": getattr(
                            provider_response.usage_metadata, "candidates_token_count", 0
                        ),
                        "total_token_count": getattr(
                            provider_response.usage_metadata, "total_token_count", 0
                        ),
                    }
                    if hasattr(provider_response, "usage_metadata")
                    and provider_response.usage_metadata
                    else {},
                    "finish_reason": getattr(provider_response, "finish_reason", None),
                }

            # Generic fallback - try to extract basic attributes
            result = {
                "text": self._extract_response_text(provider_response, provider_name),
                "provider": provider_name,
            }

            # Add usage if available
            if hasattr(provider_response, "usage") and provider_response.usage:
                usage = provider_response.usage
                result["usage"] = {}
                for attr in [
                    "prompt_tokens",
                    "completion_tokens",
                    "total_tokens",
                    "input_tokens",
                    "output_tokens",
                ]:
                    if hasattr(usage, attr):
                        result["usage"][attr] = getattr(usage, attr)

            return result

        except Exception as e:
            logger.warning(f"Failed to serialize {provider_name} response: {e}")
            # Fallback to basic text response
            return {
                "text": self._extract_response_text(provider_response, provider_name),
                "provider": provider_name,
                "serialization_error": str(e),
            }

    async def send_feedback(self, feedback: SendFeedbackProps) -> bool:
        """Send feedback for a generated response."""
        await self._ensure_session()
        http_client = self._ensure_http_client()

        try:
            # Set session_id if not provided
            if not feedback.session_id:
                feedback.session_id = self._store.session_id

            await http_client.send_feedback(feedback)
            logger.debug(f"Sent feedback for update: {feedback.update_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to send feedback: {e}")
            if self.config.on_error:
                self.config.on_error(e)
            return False

    async def update_dashboard_providers(self) -> bool:
        """Update dashboard with available providers."""
        http_client = self._ensure_http_client()

        try:
            success = await http_client.update_providers(
                product_key=self.config.product_key,
                providers=self.providers,
            )

            if success:
                logger.info("Successfully updated dashboard providers")
            else:
                logger.warning("Failed to update dashboard providers")

            return success

        except Exception as e:
            logger.error(f"Error updating dashboard providers: {e}")
            if self.config.on_error:
                self.config.on_error(e)
            return False


async def create_airbender(
    product_key: str, providers: Provider, **config_kwargs: Any
) -> AirbenderClient:
    """Factory function to create new Airbender instance."""
    config = AirbenderConfig(product_key=product_key, **config_kwargs)
    client = AirbenderClient(config, providers)
    await client.setup()
    return client


async def resume_airbender(
    session_id: str,
    providers: Provider,
    **config_kwargs: Any,
) -> tuple[AirbenderClient, str]:
    """Resume existing session and return client with product key."""
    # We need a temporary config just to fetch the session
    # We'll get the actual product_key from the session response
    temp_config = AirbenderConfig(product_key="temp", **config_kwargs)
    temp_client = AirbenderClient(temp_config, providers)

    await temp_client.setup()

    try:
        # Fetch the session to get the product key
        session = await temp_client.fetch_session_by_id(session_id)
        product_key = session.product_key

        # Now create the proper client with the correct product key
        await temp_client.close()

        config = AirbenderConfig(product_key=product_key, **config_kwargs)
        client = AirbenderClient(config, providers)
        await client.setup()

        # Set the session data directly since we already fetched it
        client._store.session_id = session.id
        client._store.session_data = session
        client._store.config = session.config
        client._store.is_blocked = session.blocked
        client._store.session_state = SessionState.SUCCESS

        return client, product_key

    except Exception:
        await temp_client.close()
        raise
