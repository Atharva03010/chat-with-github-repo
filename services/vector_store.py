import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Directory to save the database locally so it persists across server restarts
CHROMA_DB_DIR = "./chroma_db"

def vector_store_docs(raw_docs: list[dict], repo_url: str):
    """
    Takes raw code content, chunks it, and stores it in ChromaDB.
    """
    langchain_docs = []
    
    # Convert our basic dictionaries into LangChain Document objects
    for doc in raw_docs:
        metadata = {"source": doc["path"], "repo": repo_url}
        langchain_docs.append(Document(page_content=doc["content"], metadata=metadata))

    # Chunk the code
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        length_function=len
    )
    
    chunked_docs = text_splitter.split_documents(langchain_docs)
    print(f"Split {len(raw_docs)} files into {len(chunked_docs)} manageable chunks.")

    # Initialize the Embedding Model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Store in ChromaDB
    vector_store = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )
    
    return len(chunked_docs)