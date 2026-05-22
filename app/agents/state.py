from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    The state of our multi-agent graph.
    It tracks the sequence of conversation messages.
    """
    # The add_messages function ensures that new messages are 
    # appended to the existing conversation list rather than overwriting it.
    messages: Annotated[Sequence[BaseMessage], add_messages]