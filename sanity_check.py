from app.config.llm import get_llm

def test_connection():
    try:
        # Try to initialize the model using our new factory function
        llm = get_llm()
        
        print("Sending a test prompt to Qwen2.5...")
        response = llm.invoke("Say the word 'Success' and nothing else.")
        
        print("\n--- OLLAMA RESPONSE ---")
        print(response.content.strip())
        print("-----------------------")
        print("Sanity check passed perfectly!")
        
    except Exception as e:
        print("\n[ERROR] Something went wrong:")
        print(e)
        print("\nMake sure the Ollama desktop application is running on your machine!")

if __name__ == "__main__":
    test_connection()