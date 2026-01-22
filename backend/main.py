from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from .config import load_and_validate_environment, ENV

load_and_validate_environment()

chat_completion_service = OllamaChatCompletion(
    ai_model_id=ENV["OLLAMA_CHAT_MODEL_ID"],
    service_id=ENV["OLLAMA_SERVICE_ID"], # Optional; for targeting specific services within Semantic Kernel
)