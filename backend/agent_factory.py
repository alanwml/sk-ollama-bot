"""Factory for creating and configuring agents."""
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.prompt_execution_settings import PromptExecutionSettings
from config import ENV
from plugins.MenuPlugin import MenuPlugin
from prompts import MENU_AGENT_PROMPT

def _create_AzureOpenAI_chat_service() -> AzureChatCompletion:
    """Create and configure the Azure OpenAI chat completion service."""
    deployment_name = ENV["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"]
    api_key = ENV["AZURE_OPENAI_API_KEY"]
    base_url = ENV["AZURE_OPENAI_BASE_URL"]
    api_version = ENV["AZURE_OPENAI_API_VERSION"]
    return AzureChatCompletion(
                deployment_name=deployment_name,
                api_key=api_key,
                base_url=base_url,
                api_version=api_version,
                service_id="azure-openai-svc",
            )
    
def _create_Ollama_chat_service() -> OllamaChatCompletion:
    """Create and configure the Ollama chat completion service."""
    return OllamaChatCompletion(
        ai_model_id=ENV["OLLAMA_CHAT_MODEL_ID"],
        service_id=ENV["OLLAMA_SERVICE_ID"],
    )


def create_menu_agent() -> ChatCompletionAgent:
    """Create a menu recommendation agent with configured kernel and plugins."""
    kernel = Kernel()
    kernel.add_service(_create_AzureOpenAI_chat_service())
    kernel.add_plugin(plugin=MenuPlugin(), plugin_name="menu")  # Fixed: Pass an instance, not the class

    agent = ChatCompletionAgent(
        kernel=kernel,
        name="MenuAgent",
        instructions=MENU_AGENT_PROMPT,
        function_choice_behavior=FunctionChoiceBehavior.Auto(auto_invoke=True),
    )
    
    return agent
