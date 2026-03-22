import os
from dotenv import load_dotenv 
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

CHROMA_DB_DIR = "./chroma_db"
load_dotenv()  

def get_answers(user_query: str) -> dict:
    """
    Retrieves relevant code chunks from ChromaDB and uses Gemini to answer the query.
    """

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if not os.path.exists(CHROMA_DB_DIR):
        raise ValueError("Database not found. Please ingest a repository first.")
        
    vector_store = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing! Check your .env file.")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2, google_api_key=api_key) 

    # Prompt Template
    template = """You are a senior software engineer analyzing a codebase. 
    Answer the user's question based ONLY on the provided code snippets from their GitHub repository. 
    If the answer is not contained in the snippets, clearly state: "I cannot find the answer in the provided repository context."
    Include the file paths of the code you are referencing in your answer.

    Code Context:
    {context}

    User Question: {input}

    Answer:"""
    
    prompt = PromptTemplate.from_template(template)

    # Build the RAG Chain
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    # Execute the query
    response = retrieval_chain.invoke({"input": user_query})
    
    return {
        "answer": response["answer"],
        "sources": [doc.metadata.get("source", "Unknown file") for doc in response["context"]]
    }