import os
from typing import Any
from dotenv import load_dotenv

# === ENV Setup ===
ENV: dict[str, Any] = {
    "OLLAMA_CHAT_MODEL_ID": None,
    "OLLAMA_HOST": None,
    "OLLAMA_SERVICE_ID": None,
    "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": None,
    "AZURE_OPENAI_API_KEY": None,
    "AZURE_OPENAI_BASE_URL": None,
    "AZURE_OPENAI_API_VERSION": None,
}

def load_and_validate_environment():
    """Load and validate environment variables."""
    load_dotenv()  # Load variables from .env file if present
    for key, value in ENV.items():
        new_value = os.getenv(key)
        if new_value is not None:
            ENV[key] = new_value
        elif value is None:
            raise ValueError(f"Environment variable {key} not set")