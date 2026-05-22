from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from app.config.llm import get_llm
from app.tools.actions import agent_tools
from app.agents.state import AgentState

# 1. Initialize our customizable LLM and bind our tools to it
llm = get_llm()
llm_with_tools = llm.bind_tools(agent_tools)

# 2. Define our core Core Router Node
def core_router_node(state: AgentState):
    """
    This node takes the current conversation state, passes it to the LLM,
    and returns the LLM's response (whether it's plain text or a tool call).
    """
    print("\n--- [NODE] Core Router Processing State ---")
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 3. Define the routing logic condition
def route_decision(state: AgentState):
    """
    This conditional function checks if the last message from the LLM
    wanted to trigger a tool call. If yes, it routes to our tools. If no, it ends.
    """
    last_message = state["messages"][-1]
    
    if last_message.tool_calls:
        print(f" -> [ROUTER] Directing to Tool Execution: {last_message.tool_calls[0]['name']}")
        return "execute_tools"
        
    print(" -> [ROUTER] Final text response ready. Ending graph execution.")
    return END

# 4. Construct the Graph Workflow
workflow = StateGraph(AgentState)

# Add our core nodes
workflow.add_node("router", core_router_node)
workflow.add_node("execute_tools", ToolNode(agent_tools)) # Prebuilt node that automatically runs our Python tools

# Establish connections (edges)
workflow.add_edge(START, "router")

# Add conditional routing out of our router node
workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "execute_tools": "execute_tools",
        "__end__": END
    }
)

# Connect the tools node back to the router so the model can inspect the tool's output
workflow.add_edge("execute_tools", "router")

# Compile our graph into an executable application
agent_app = workflow.compile()