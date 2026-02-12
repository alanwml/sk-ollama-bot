"""Logging utilities for capturing agent thoughts and interactions."""
import logging
import contextvars
from typing import Dict, List, Optional

current_conversation_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "current_conversation_id", default=""
)


class CapturingHandler(logging.Handler):
    """Custom handler that captures logs per conversation ID."""
    
    def __init__(self):
        super().__init__()
        # Buffer logs per conversation id
        self._buffers: Dict[str, List[str]] = {}

    def emit(self, record):
        conv_id = current_conversation_id.get()
        if conv_id is None:
            # Fallback to a default buffer if no conversation id is set
            conv_id = "__default__"
        msg = self.format(record)
        self._buffers.setdefault(conv_id, []).append(msg)

    def get_logs(self, conv_id: Optional[str] = None) -> List[str]:
        """Get captured logs for a specific conversation."""
        if conv_id is None:
            conv_id = current_conversation_id.get()
            if conv_id is None:
                conv_id = "__default__"
        return self._buffers.get(conv_id, [])

    def clear(self, conv_id: Optional[str] = None):
        """Clear logs for a specific conversation."""
        if conv_id is None:
            conv_id = current_conversation_id.get()
            if conv_id is None:
                conv_id = "__default__"
        self._buffers.pop(conv_id, None)


def setup_agent_logging() -> CapturingHandler:
    """Configure logging for agent interactions and reasoning."""
    capturing_handler = CapturingHandler()
    capturing_handler.setFormatter(
        logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    )

    agent_logger = logging.getLogger("semantic_kernel")
    agent_logger.setLevel(logging.DEBUG)
    # Clear any existing handlers to prevent duplicates on re-runs
    agent_logger.handlers.clear()
    agent_logger.addHandler(capturing_handler)

    # Suppress prompt template logs
    logging.getLogger("semantic_kernel.prompt_template.kernel_prompt_template").setLevel(
        logging.WARNING
    )
    
    return capturing_handler
