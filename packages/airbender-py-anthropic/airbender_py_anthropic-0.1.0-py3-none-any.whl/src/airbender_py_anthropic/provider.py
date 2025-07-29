"""Anthropic provider implementation for Airbender Python SDK."""

from typing import Any, Protocol

import anthropic


class ProviderProtocol(Protocol):
    """Protocol that all Airbender providers must implement."""

    def supported_models(self) -> list[str]:
        """Return list of supported models for this provider."""
        ...

    async def generate_text(
        self,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any
    ) -> Any:
        """Generate text using this provider."""
        ...

    async def stream_text(
        self,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any
    ) -> Any:
        """Stream text using this provider."""
        ...


class AnthropicProvider:
    """Anthropic provider implementation."""

    def __init__(self, api_key: str | None = None, **kwargs: Any):
        """Initialize Anthropic provider."""
        self.client = anthropic.AsyncAnthropic(api_key=api_key, **kwargs)

    def supported_models(self) -> list[str]:
        """Return list of supported Anthropic models."""
        return [
            "claude-3-haiku-20240307",
            "claude-3-7-sonnet-20250219"
        ]

    async def generate_text(
        self,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any
    ) -> Any:
        """Generate text using Anthropic."""
        if model not in self.supported_models():
            raise ValueError(
                f"Model {model} not supported. Supported models: {self.supported_models()}"
            )

        # Convert messages to Anthropic format if needed
        anthropic_messages = self._convert_messages(messages)

        response = await self.client.messages.create(
            model=model,
            messages=anthropic_messages,  # type: ignore[arg-type]
            **kwargs
        )
        return response

    async def stream_text(
        self,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any
    ) -> Any:
        """Stream text using Anthropic."""
        if model not in self.supported_models():
            raise ValueError(
                f"Model {model} not supported. Supported models: {self.supported_models()}"
            )

        # Convert messages to Anthropic format if needed
        anthropic_messages = self._convert_messages(messages)

        stream = await self.client.messages.create(
            model=model,
            messages=anthropic_messages,  # type: ignore[arg-type]
            stream=True,
            **kwargs
        )
        return stream

    def _convert_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Convert messages to Anthropic format.

        Anthropic requires system messages to be handled differently than user/assistant messages.
        """
        anthropic_messages = []

        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            # Anthropic uses the same message format as OpenAI for user/assistant
            # System messages are handled separately in the API call
            if role in ["user", "assistant"]:
                anthropic_messages.append({
                    "role": role,
                    "content": content
                })
            # Note: System messages should be passed as 'system' parameter to messages.create()
            # For now, we'll include them in messages but this might need adjustment
            elif role == "system":
                anthropic_messages.append({
                    "role": "user",  # Convert system to user for compatibility
                    "content": f"System: {content}"
                })

        return anthropic_messages


def supported_models() -> list[str]:
    """Return list of supported Anthropic models."""
    return [
        "claude-3-haiku-20240307",
        "claude-3-7-sonnet-20250219"
    ]


def init(api_key: str | None = None, **kwargs: Any) -> AnthropicProvider:
    """
    Initialize Anthropic provider.

    Args:
        api_key: Anthropic API key (if not provided, uses environment)
        **kwargs: Additional arguments passed to Anthropic client

    Returns:
        Configured Anthropic provider instance
    """
    return AnthropicProvider(api_key=api_key, **kwargs)
