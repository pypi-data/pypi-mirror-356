"""Google Generative AI provider implementation for Airbender Python SDK."""

from typing import Any, Protocol

import google.generativeai as genai


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


class GoogleProvider:
    """Google Generative AI provider implementation."""

    def __init__(self, api_key: str | None = None, **kwargs: Any):
        """Initialize Google provider."""
        if api_key:
            genai.configure(api_key=api_key)  # type: ignore[attr-defined]
        # Additional configuration can be added via kwargs if needed
        self._config_kwargs = kwargs

    def supported_models(self) -> list[str]:
        """Return list of supported Google models."""
        return [
            "gemini-1.5-flash-8b",
            "gemini-1.5-pro-latest",
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite"
        ]

    async def generate_text(
        self,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any
    ) -> Any:
        """Generate text using Google Generative AI."""
        if model not in self.supported_models():
            raise ValueError(
                f"Model {model} not supported. Supported models: {self.supported_models()}"
            )

        # Convert messages to Google format
        google_messages = self._convert_messages_to_google(messages)

        # Extract and convert common parameters to Google format
        google_kwargs = self._convert_kwargs_to_google(kwargs)

        # Create the model instance
        model_instance = genai.GenerativeModel(model)  # type: ignore[attr-defined]

        # Generate content
        response = await model_instance.generate_content_async(
            google_messages,
            **google_kwargs
        )
        return response

    async def stream_text(
        self,
        model: str,
        messages: list[dict[str, Any]],
        **kwargs: Any
    ) -> Any:
        """Stream text using Google Generative AI."""
        if model not in self.supported_models():
            raise ValueError(
                f"Model {model} not supported. Supported models: {self.supported_models()}"
            )

        # Convert messages to Google format
        google_messages = self._convert_messages_to_google(messages)

        # Extract and convert common parameters to Google format
        google_kwargs = self._convert_kwargs_to_google(kwargs)

        # Create the model instance
        model_instance = genai.GenerativeModel(model)  # type: ignore[attr-defined]

        # Generate streaming content
        stream = await model_instance.generate_content_async(
            google_messages,
            stream=True,
            **google_kwargs
        )
        return stream

    def _convert_messages_to_google(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Convert messages to Google Generative AI format.

        Google uses a simpler format where:
        - 'user' messages are input from the user
        - 'model' messages are responses from the AI (instead of 'assistant')
        - 'system' messages need to be handled as part of the conversation
        """
        google_messages = []

        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            if role == "user":
                google_messages.append({
                    "role": "user",
                    "parts": [{"text": content}]
                })
            elif role == "assistant":
                # Google uses 'model' instead of 'assistant'
                google_messages.append({
                    "role": "model",
                    "parts": [{"text": content}]
                })
            elif role == "system":
                # Convert system message to user message with system prefix
                google_messages.append({
                    "role": "user",
                    "parts": [{"text": f"System instruction: {content}"}]
                })

        return google_messages

    def _convert_kwargs_to_google(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Convert common LLM parameters to Google Generative AI format.

        Google uses a generation_config object for parameters like temperature, max_tokens, etc.
        """
        google_kwargs = {}
        generation_config = {}

        # Map common parameters to Google's generation_config
        if 'temperature' in kwargs:
            generation_config['temperature'] = kwargs['temperature']

        if 'max_tokens' in kwargs:
            generation_config['max_output_tokens'] = kwargs['max_tokens']

        if 'top_p' in kwargs:
            generation_config['top_p'] = kwargs['top_p']

        # Add other supported parameters that don't go in generation_config
        if 'stream' in kwargs:
            google_kwargs['stream'] = kwargs['stream']

        # Add generation_config if we have any parameters
        if generation_config:
            google_kwargs['generation_config'] = generation_config

        return google_kwargs


def supported_models() -> list[str]:
    """Return list of supported Google models."""
    return [
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro-latest",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite"
    ]


def init(api_key: str | None = None, **kwargs: Any) -> GoogleProvider:
    """
    Initialize Google Generative AI provider.

    Args:
        api_key: Google API key (if not provided, uses environment)
        **kwargs: Additional configuration arguments

    Returns:
        Configured Google provider instance
    """
    return GoogleProvider(api_key=api_key, **kwargs)
