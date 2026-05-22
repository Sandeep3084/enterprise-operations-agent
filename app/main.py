from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from langchain_core.messages import HumanMessage, AIMessage
from app.agents.graph import agent_app

app = FastAPI(
    title="Autonomous Enterprise Operations Platform",
    description="Production-grade multi-agent backend engine utilizing LangGraph, FastAPI, and Vector RAG.",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "frameworks": ["FastAPI", "LangGraph", "ChromaDB", "Groq"]
    }

@app.post("/chat")
async def chat_with_agent(payload: ChatRequest):
    try:
        print(f"\n[API RECEIVE] Processing conversation history: {len(payload.messages)} messages")
        
        formatted_messages = []
        for msg in payload.messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                formatted_messages.append(AIMessage(content=msg["content"]))
        
        initial_state = {
            "messages": formatted_messages
        }
        
        graph_output = agent_app.invoke(initial_state)
        final_response_message = graph_output["messages"][-1]
        
        return {
            "success": True,
            "response": final_response_message.content
        }
        
    except Exception as e:
        print(f"[API ERROR] Execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")