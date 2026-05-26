# Autonomous Enterprise Operations Engine

A production-grade, multi-agent architecture designed to handle dynamic enterprise operations autonomously. Powered by LangGraph, FastAPI, and Groq's high-speed inference, this engine intelligently routes user intents, retrieves corporate policies via Local Vector RAG, and executes live operational tools in real time.

## System Architecture

This project strictly decouples the user interface from the reasoning engine, ensuring the backend can be scaled independently or consumed by other microservices.

<img width="1013" height="591" alt="image" src="https://github.com/user-attachments/assets/f4f7ecb8-b5d9-4c7e-8ed1-c1ccb11e7dfa" />


### 1. The Reasoning Engine (LangGraph + Groq)
At the core is a stateful cyclical graph built with **LangGraph**. 
* **State Management:** Maintains a continuous global `AgentState` containing the exact chronological array of messages (`HumanMessage`, `AIMessage`, `ToolMessage`), solving the "conversational amnesia" problem.
* **Dynamic Routing:** A conditional edge router intercepts the LLM's output. If the Llama 3.3 70B model determines a tool is needed, the graph temporarily halts direct output, routes to the `ToolNode`, executes the raw Python function, appends the result to the state, and loops back to the LLM for final synthesis.
* **Guardrail Bypassing:** Utilizes runtime `SystemMessage` injection to override standard base-model refusals, forcing strict compliance for internal policy retrieval without mutating the permanent state logs.

### 2. Semantic RAG Pipeline (ChromaDB)
* Implements a local, fully embedded vector database using **Chroma**.
* Converts unstructured enterprise data (e.g., `company_faq.txt`) into dense vector embeddings.
* Resolves absolute container pathing dynamically (`os.path.abspath`), ensuring the database is instantly readable across both local Windows/Linux machines and serverless cloud containers without rebuilds.

### 3. API Gateway (FastAPI)
* Wraps the LangGraph reasoning engine in an asynchronous REST API.
* Handles data validation via **Pydantic** models, ensuring incoming conversation histories are properly formatted before being cast into LangChain message objects.

### 4. Client Dashboard (Streamlit)
* A session-state persistent user interface that handles real-time HTTP requests to the FastAPI backend.
* Renders agent tool actions, execution spinners, and Markdown-formatted output for a seamless operational experience.

---

## Core Capabilities

* **Internal Policy Retrieval (RAG):** Answers queries regarding compliance, refunds, and corporate rules by bypassing safety blocks and conducting similarity searches against the embedded corporate database.
* **Live Web Crawling:** Ingests raw URLs, scrapes text content in real time, and synthesizes it for competitive analysis or account evaluations.
* **CRM Lead Qualification:** Programmatically extracts structured entity data (Company Name, Email, Employee Count) from natural conversation and pushes it to backend tracking workflows.
* **Order Tracking:** Validates customer IDs and tracks logistics statuses via dynamic tool execution.

---

## Tech Stack

* **LLM:** Llama-3.3-70b-versatile (via Groq API)
* **Agent Framework:** LangGraph, LangChain
* **Vector Database:** ChromaDB 
* **Backend:** FastAPI, Uvicorn, Python 3.10+
* **Frontend:** Streamlit
* **Deployment Architecture:** Render (Backend API) + Streamlit Community Cloud (Frontend UI)

---

## Local Setup & Installation

### 1. Clone the Repository
```
git clone [https://github.com/yourusername/enterprise-operations-engine.git](https://github.com/yourusername/enterprise-operations-engine.git)
cd enterprise-operations-engine
```

### 2. Create and activate the virtual environment 
```
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependancies 
```
pip install -r requirements.txt
```

### 4. Start the backend API
```
uvicorn app.main:app --reload
```

### 5. Start the frontend UI (in a new terminal)
```
.\venv\Scripts\activate
streamlit run frontend/app.py
```
