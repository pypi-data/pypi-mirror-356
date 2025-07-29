"""HTTP client for Airbender API."""

import asyncio
from typing import Any

import httpx

from ..config import AirbenderConfig
from ..models import Provider, SendFeedbackProps, SessionAPIResponse


class APIError(Exception):
    """API error exception."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AirbenderHTTPClient:
    """HTTP client for Airbender API communication."""

    def __init__(self, config: AirbenderConfig):
        self.config = config
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_client()
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        """Async context manager exit."""
        await self.close()

    async def _ensure_client(self) -> httpx.AsyncClient:
        """Ensure HTTP client is initialized."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.config.timeout),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "airbender-py-client/0.1.0",
                },
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make HTTP request with retry logic."""
        client = await self._ensure_client()
        url = f"{self.config.api_base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        last_exception: Exception | None = None
        for attempt in range(self.config.max_retries + 1):
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                )

                if response.status_code >= 400:
                    error_data = {}
                    try:
                        error_data = response.json()
                    except Exception:
                        pass

                    error_message = error_data.get("message", f"HTTP {response.status_code}")
                    raise APIError(error_message, response.status_code)

                return response.json()  # type: ignore[no-any-return]

            except httpx.RequestError as e:
                last_exception = e
                if attempt < self.config.max_retries:
                    await asyncio.sleep(2**attempt)  # Exponential backoff
                    continue
                raise APIError(f"Request failed: {str(e)}") from e
            except APIError:
                raise
            except Exception as e:
                last_exception = e
                if attempt < self.config.max_retries:
                    await asyncio.sleep(2**attempt)
                    continue
                raise APIError(f"Unexpected error: {str(e)}") from e

        # This should never be reached, but just in case
        if last_exception:
            raise APIError(
                f"Request failed after {self.config.max_retries} retries: {str(last_exception)}"
            )

        raise APIError("Request failed for unknown reason")

    async def create_session(self, product_key: str, user: str | None = None) -> SessionAPIResponse:
        """Create a new session."""
        data = {"productKey": product_key}
        if user:
            data["user"] = user

        response_data = await self._request("POST", "/session", data=data)
        return SessionAPIResponse.model_validate(response_data)

    async def fetch_session(self, session_id: str) -> SessionAPIResponse:
        """Fetch an existing session."""
        response_data = await self._request("GET", f"/session/{session_id}")
        return SessionAPIResponse.model_validate(response_data)

    async def send_feedback(self, feedback: SendFeedbackProps) -> dict[str, Any]:
        """Send feedback for a generated response."""
        data = feedback.model_dump(by_alias=True, exclude_none=True)

        # Transform update_id to logId for API compatibility
        if "updateId" in data:
            data["logId"] = data.pop("updateId")

        return await self._request("POST", "/feedback", data=data)

    async def update_providers(self, product_key: str, providers: Provider) -> bool:
        """Update dashboard with available providers."""
        # Convert provider instances to the format expected by the API
        provider_data = {}
        for provider_name, provider_instance in providers.items():
            provider_data[provider_name] = provider_instance.supported_models()

        data = {
            "productKey": product_key,
            "providers": provider_data,
        }

        try:
            await self._request("POST", "/product-providers", data=data)
            return True
        except APIError:
            return False

    async def generate_text(
        self,
        product_key: str,
        session_id: str,
        airbender_agent: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Generate text using specified agent."""
        data = {
            "productKey": product_key,
            "sessionId": session_id,
            "airbenderAgent": airbender_agent,
            **kwargs,
        }

        return await self._request("POST", "/api/airbender/gentext", data=data)

    async def stream_text(
        self,
        product_key: str,
        session_id: str,
        airbender_agent: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Stream text using specified agent."""
        data = {
            "productKey": product_key,
            "sessionId": session_id,
            "airbenderAgent": airbender_agent,
            **kwargs,
        }

        return await self._request("POST", "/api/airbender/streamText", data=data)

    async def create_log(
        self,
        session_id: str,
        airbender_agent: str,
        model: str,
        provider: str,
        input_data: Any = None,
        output_data: Any = None,
        dynamic_model: bool = True,
        system_prompt: str | None = None,
        control_point_id: str | None = None,
    ) -> dict[str, Any]:
        """Create or update a log entry using the /api/v1/log endpoint."""
        data = {
            "sessionId": session_id,
            "input": input_data,
            "output": output_data,
            "model": model,
            "provider": provider,
            "logName": airbender_agent,
            "dynamicModel": dynamic_model,
            "systemPrompt": system_prompt,
            "controlPointId": control_point_id,
        }

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        return await self._request("POST", "/log", data=data)
