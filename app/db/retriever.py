import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Define path for persisting our vector database locally
CHROMA_DIR = "./chroma_db"

def init_knowledge_base():
    """
    Reads local text documents, creates semantic vector embeddings,
    and stores them inside a local Chroma DB instance.
    """
    faq_path = "app/data/company_faq.txt"
    if not os.path.exists(faq_path):
        raise FileNotFoundError(f"Knowledge source file missing at {faq_path}")
        
    print("[RAG CONFIG] Ingesting source documentation text...")
    loader = TextLoader(faq_path)
    documents = loader.load()
    
    # Split the document into small chunks so search results are hyper-focused
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = text_splitter.split_documents(documents)
    
    print("[RAG CONFIG] Initializing Ollama Embeddings (nomic-embed-text)...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    print(f"[RAG CONFIG] Storing {len(chunks)} chunks securely inside ChromaDB at '{CHROMA_DIR}'...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    return vectorstore

def get_retriever():
    """
    Returns an active retriever interface to query the stored database.
    """
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    # Load the already existing database from disk
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 2}) # Retrieve top 2 most relevant matches

if __name__ == "__main__":
    # Initialize the database when this script is run directly
    init_knowledge_base()