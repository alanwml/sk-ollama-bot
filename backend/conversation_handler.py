"""Handles conversation flow and agent interactions."""
import logging
from typing import List
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.completion_usage import CompletionUsage
from semantic_kernel.contents import ChatMessageContent, FunctionCallContent, FunctionResultContent

agent_logger = logging.getLogger("semantic_kernel")

def _write_content(content: ChatMessageContent) -> None:
    """Write the content to the console based on the content type."""
    last_item_type = type(content.items[-1]).__name__ if content.items else "(empty)"
    message_content = ""
    if isinstance(last_item_type, FunctionCallContent):
        message_content = f"tool request = {content.items[-1].function_name}"
    elif isinstance(last_item_type, FunctionResultContent):
        message_content = f"function result = {content.items[-1].result}"
    else:
        message_content = str(content.items[-1])
    print(f"[{last_item_type}] {content.role} : '{message_content}'")

async def run_conversation(
    agent: ChatCompletionAgent,
    user_inputs: List[str],
    thread: ChatHistoryAgentThread
) -> tuple[ChatHistoryAgentThread, CompletionUsage]:
    """
    Run a conversation with the agent for multiple user inputs.
    
    Returns:
        Tuple of (updated thread, total completion usage)
    """
    completion_usage = CompletionUsage()
    
    # for user_input in user_inputs:
    #     print(f"\n# User: '{user_input}'")
    #     agent_logger.info(f"[User Input]: {user_input}")
        
    #     full_response = ""
    #     async for response in agent.invoke_stream(
    #         messages=user_input,
    #         thread=thread,
    #     ):
    #         if response.content:
    #             print(response.content, end="", flush=True)
    #             full_response += str(response.content)
                
    #         if response.metadata.get("usage"):
    #             completion_usage += response.metadata["usage"]
    #             agent_logger.info(f"[Token Usage]: {response.metadata['usage']}")
    #             agent_logger.info(f"[Model Usage]: {response.metadata['model']}")
    #         thread = response.thread
        
    #     # Log the complete response after streaming
    #     if full_response:
    #         agent_logger.info(f"[Agent Response]: {full_response}")

    #     print()

    for user_input in user_inputs:
        print(f"# User: '{user_input}'")
        response = await agent.get_response(messages=user_input, thread=thread)
        thread = response.thread
        _write_content(response)

        print()
    
    return thread, completion_usage


async def print_chat_history(thread: ChatHistoryAgentThread) -> None:
    """Print the complete chat history from a thread."""
    print("\n=== Complete Chat History ===")
    async for msg in thread.get_messages():
        _write_content(msg)
