import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

# Load the variables from your hidden .env file
load_dotenv()

def get_llm():
    """
    Factory function that looks at the .env file 
    and returns the configured language model.
    """
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    
    if provider == "ollama":
        model_name = os.getenv("OLLAMA_MODEL", "qwen2.5")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        print(f"[LLM CONFIG] Initializing local model '{model_name}' via Ollama...")
        
        return ChatOllama(
            model=model_name,
            base_url=base_url,
            temperature=0.2
        )
        
    elif provider == "groq":
        model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key or api_key == "gsk_paste_your_real_key_here":
            raise ValueError("Groq API key is missing or invalid in the .env file!")
            
        print(f"[LLM CONFIG] Initializing cloud model '{model_name}' via Groq...")
        
        return ChatGroq(
            model=model_name,
            api_key=api_key,
            temperature=0.2
        )
        
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")