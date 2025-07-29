"""OpenAI provider implementation for Airbender Python SDK."""

from typing import Any, Protocol

import openai


class ProviderProtocol(Protocol):
    """Protocol that all Airbender providers must implement."""

    def supported_models(self) -> list[str]:
        """Return list of supported models for this provider."""
        ...

    async def generate_text(self, model: str, messages: list[dict[str, Any]], **kwargs: Any) -> Any:
        """Generate text using this provider."""
        ...

    async def stream_text(self, model: str, messages: list[dict[str, Any]], **kwargs: Any) -> Any:
        """Stream text using this provider."""
        ...


class OpenAIProvider:
    """OpenAI provider implementation."""

    def __init__(self, api_key: str | None = None, **kwargs: Any):
        """Initialize OpenAI provider."""
        self.client = openai.AsyncOpenAI(api_key=api_key, **kwargs)

    def supported_models(self) -> list[str]:
        """Return list of supported OpenAI models."""
        return ["gpt-4o", "gpt-4-turbo", "gpt-4o-mini"]

    async def generate_text(self, model: str, messages: list[dict[str, Any]], **kwargs: Any) -> Any:
        """Generate text using OpenAI."""
        if model not in self.supported_models():
            raise ValueError(
                f"Model {model} not supported. Supported models: {self.supported_models()}"
            )

        response = await self.client.chat.completions.create(
            model=model, messages=messages, **kwargs  # type: ignore[arg-type]
        )
        return response

    async def stream_text(self, model: str, messages: list[dict[str, Any]], **kwargs: Any) -> Any:
        """Stream text using OpenAI."""
        if model not in self.supported_models():
            raise ValueError(
                f"Model {model} not supported. Supported models: {self.supported_models()}"
            )

        stream = await self.client.chat.completions.create(
            model=model, messages=messages, stream=True, **kwargs  # type: ignore[arg-type]
        )
        return stream


def supported_models() -> list[str]:
    """Return list of supported OpenAI models."""
    return ["gpt-4o", "gpt-4-turbo", "gpt-4o-mini"]


def init(api_key: str | None = None, **kwargs: Any) -> OpenAIProvider:
    """
    Initialize OpenAI provider.

    Args:
        api_key: OpenAI API key (if not provided, uses environment)
        **kwargs: Additional arguments passed to OpenAI client

    Returns:
        Configured OpenAI provider instance
    """
    return OpenAIProvider(api_key=api_key, **kwargs)
