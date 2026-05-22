from app.config.llm import get_llm
from app.tools.actions import agent_tools

def verify_tool_binding():
    print("Initializing LLM...")
    llm = get_llm()
    
    # Bind our tools to the language model
    llm_with_tools = llm.bind_tools(agent_tools)
    
    # Let's test if the model can identify a customer who wants to buy something
    test_prompt = "Hi, my name is John. I represent a company of 120 employees and we want to purchase your enterprise tier. Contact me at john@enterprise.com"
    
    print(f"\nSending prompt to model: '{test_prompt}'")
    response = llm_with_tools.invoke(test_prompt)
    
    print("\n--- Model Evaluation ---")
    if response.tool_calls:
        print("SUCCESS! The model autonomously chose to trigger a tool execution:")
        for tool_call in response.tool_calls:
            print(f" -> Tool Picked: {tool_call['name']}")
            print(f" -> Arguments Extracted: {tool_call['args']}")
    else:
        print("The model just gave a normal text reply instead of picking a tool.")
        print(f"Reply: {response.content}")

if __name__ == "__main__":
    verify_tool_binding()