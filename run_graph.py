from app.agents.graph import agent_app
from langchain_core.messages import HumanMessage

def test_full_graph_loop():
    print("Starting LangGraph multi-agent simulation...")
    
    # Simulate a user message
    initial_state = {
        "messages": [HumanMessage(content="Hi, please check the status of my order ORD-123.")]
    }
    
    # Run the graph synchronously
    final_output = agent_app.invoke(initial_state)
    
    print("\n================ FINAL RESPONSE ================")
    print(final_output["messages"][-1].content)
    print("=================================================")

if __name__ == "__main__":
    test_full_graph_loop()