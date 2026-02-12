"""Factory for creating and configuring agents."""
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from config import ENV
from plugins import MenuPlugin
from prompts import MENU_AGENT_PROMPT


def _create_chat_service() -> OllamaChatCompletion:
    """Create and configure the Ollama chat completion service."""
    return OllamaChatCompletion(
        ai_model_id=ENV["OLLAMA_CHAT_MODEL_ID"],
        service_id=ENV["OLLAMA_SERVICE_ID"],
    )


def create_menu_agent() -> ChatCompletionAgent:
    """Create a menu recommendation agent with configured kernel and plugins."""
    kernel = Kernel()
    kernel.add_service(_create_chat_service())
    kernel.add_plugin(plugin=MenuPlugin, plugin_name="menu")

    agent = ChatCompletionAgent(
        kernel=kernel,
        name="MenuAgent",
        instructions=MENU_AGENT_PROMPT
    )
    
    return agent
