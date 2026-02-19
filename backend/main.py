"""Main entry point for the Ollama chatbot."""
import asyncio
from semantic_kernel.agents import ChatHistoryAgentThread
from semantic_kernel.agents.azure_ai.azure_ai_agent import AzureAIAgent, AzureAIAgentThread
from config import load_and_validate_environment
from logging_utils import setup_agent_logging, current_conversation_id
from agent_factory import create_menu_agent
from conversation_handler import run_conversation, print_chat_history

load_and_validate_environment()


async def main() -> None:
    """Run the chatbot with predefined test inputs."""
    # Setup logging
    capturing_handler = setup_agent_logging()
    capturing_handler.clear()
    
    # Create agent and conversation thread
    agent = create_menu_agent()
    thread = await AzureAIAgentThread.create(thread_id="thread-1")
    
    if thread.id:
        current_conversation_id.set(thread.id)
        print(thread.id)
        async for msg in thread.get_messages():
            print(f"Thread Message: {msg}")
    
    # Define test inputs
    user_inputs = [
        "Hello",
        "What is the special soup?",
        "How much does that cost?",
        "Thank you",
        "What were my previous questions?",
        "What is 1 + 0?"
    ]
    
    # Run conversation
    thread, completion_usage = await run_conversation(agent, user_inputs, thread)
    
    # Print results
    print(f"\nStreaming Total Completion Usage: {completion_usage.model_dump_json(indent=4)}")
    await print_chat_history(thread)
    
    print("\n=== Captured Thoughts ===")
    for thought in capturing_handler.get_logs():
        print(thought)


if __name__ == "__main__":
    asyncio.run(main())