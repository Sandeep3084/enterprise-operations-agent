from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from app.config.llm import get_llm
from app.tools.actions import agent_tools
from app.agents.state import AgentState

# Initialize model and bind tools
llm = get_llm()
llm_with_tools = llm.bind_tools(agent_tools)

# Explicit prompt directing model to prioritize tool usage for policies
SYSTEM_PROMPT = """
You are the primary automated operations agent for Nexus Enterprise Solutions. 

CRITICAL INSTRUCTION: You MUST use the `query_company_knowledge` tool to answer ANY questions regarding company policies, refunds, or guidelines. 
Do NOT refuse to answer policy questions. Do NOT tell the user to contact a representative. Always fetch the policy from your tools and summarize it for the user.
"""

# Core reasoning node that injects the system instructions before invocation
def call_model(state: AgentState):
    messages = state["messages"]
    modified_messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    response = llm_with_tools.invoke(modified_messages)
    return {"messages": [response]}

# Execution node for running python functions triggered by the agent
tool_node = ToolNode(agent_tools)

# Evaluates whether the agent requires a tool or is ready to reply
def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# Graph compilation and layout architecture definition
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

agent_app = workflow.compile()