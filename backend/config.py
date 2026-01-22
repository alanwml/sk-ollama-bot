import os
from typing import Any
from dotenv import load_dotenv

# === ENV Setup ===
ENV: dict[str, Any] = {
    "OLLAMA_CHAT_MODEL_ID": None,
    "OLLAMA_HOST": None,
    "OLLAMA_SERVICE_ID": None,
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