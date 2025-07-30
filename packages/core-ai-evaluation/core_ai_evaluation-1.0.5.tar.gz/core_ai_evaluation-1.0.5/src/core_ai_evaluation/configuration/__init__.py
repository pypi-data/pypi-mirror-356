import os

from src.configuration.azure import AzureOpenAIProvider
from src.configuration.gemini import GeminiProvider
from src.configuration.ollama import OllamaProvider
from src.configuration.provider import ModelProvider
from src.configuration.vertex_ai_anthropic import VertexAIAnthropicProvider


def get_all_providers() -> list[ModelProvider]:
    """
    Get all available providers.
    """
    return [
        GeminiProvider(),
        AzureOpenAIProvider(),
        VertexAIAnthropicProvider(),
        OllamaProvider(),
    ]


def get_available_providers() -> list[ModelProvider]:
    return [p for p in get_all_providers() if p.requirements_met]


def get_provider_environment_variables() -> dict[str, str]:
    env_vars = ""
    for p in get_all_providers():
        env_vars += f"Provider: {p.__class__.__name__}\n"
        for var in p.return_required_env_vars():
            env_vars += f"  - {var}: {os.getenv(var)}\n"

    return env_vars
