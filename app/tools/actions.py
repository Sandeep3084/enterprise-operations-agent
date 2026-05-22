from langchain_core.tools import tool

@tool
def check_order_status(order_id: str) -> str:
    """
    Use this tool to check the current status of an e-commerce order.
    This tool requires a valid order_id string format starting with 'ORD-'.
    """
    # Just a prototype, so simulating a database query rather than calling an API.
    print(f"\n[TOOL LOG] Running check_order_status for: {order_id}...")
    
    mock_shopify_db = {
        "ORD-123": "Status: Shipped. Package is with DHL and will arrive in 2 business days.",
        "ORD-456": "Status: Processing. Items are being packed in the warehouse.",
        "ORD-789": "Status: Delivered. Left at the front door yesterday."
    }
    
    return mock_shopify_db.get(order_id, f"Order ID '{order_id}' was not found in the system.")


@tool
def qualify_lead(email: str, company_size: int) -> str:
    """
    Use this tool when a user or client wants to buy software or book a business demo.
    It requires the user's business email and the size of their company.
    """
    # In a real enterprise application, this would execute an API POST request to HubSpot CRM.
    print(f"\n[TOOL LOG] Pushing new lead details to HubSpot CRM: {email} (Size: {company_size})...")
    
    if company_size > 50:
        return f"Lead successfully saved to CRM as HIGH PRIORITY. Automatically generated VIP booking link: https://calendly.com/stepsai-vip-demo"
    else:
        return f"Lead saved to CRM. Standard onboarding email sent to {email}."


# Put all the available tools into a clean list that it can pass to the agents later.
agent_tools = [check_order_status, qualify_lead]

from app.db.retriever import get_retriever

@tool
def query_company_knowledge(query: str) -> str:
    """
    Use this tool to search internal company documentation for answers regarding 
    company policies, refunds, data privacy standards, and system schedules.
    """
    print(f"\n[TOOL LOG] Performing vector database semantic search for: '{query}'...")
    try:
        retriever = get_retriever()
        relevant_docs = retriever.invoke(query)
        
        # Combine retrieved text chunks into a single reference context string
        context = "\n".join([doc.page_content for doc in relevant_docs])
        return f"Found matching internal records:\n{context}"
    except Exception as e:
        return f"Failed to retrieve company data records: {str(e)}"

# Update the main tool exports list to include the RAG search tool
agent_tools = [check_order_status, qualify_lead, query_company_knowledge]

import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from app.db.retriever import get_retriever

@tool
def scrape_company_website(url: str) -> str:
    """
    Use this tool to crawl and scrape a company's website to understand their core product, 
    industry, or target audience. Requires a valid URL string starting with http:// or https://.
    """
    print(f"\n[TOOL LOG] Initiating live web crawl for: {url}...")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.extract()

        # Extract the visible text and clean up the massive blank spaces
        text = soup.get_text(separator=' ')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # truncate the output to 1500 characters to protect the llm's context window 
        # while still capturing the homepage hero text and about sections.
        return f"Successfully scraped {url}. Website content:\n{cleaned_text[:1500]}..."
        
    except Exception as e:
        return f"Failed to scrape {url}. Error: {str(e)}"

# update exports list at the very bottom to include the new tool :-)
agent_tools = [check_order_status, qualify_lead, query_company_knowledge, scrape_company_website]