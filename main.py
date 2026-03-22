from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.github_ingestor import clone_and_parse_repo
from services.vector_store import vector_store_docs

# Initialize the FastAPI application
app = FastAPI(
    title="Chat with Repo API",
    description="An API to ingest GitHub repositories and query them using RAG.",
    version="1.0.0"
)

# --- Data Validation Models ---

class RepoRequest(BaseModel):
    repo_url: str

class ChatRequest(BaseModel):
    query: str

# --- API Endpoints ---

@app.get("/")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "active", "message": "Chat with Repo API is running. Visit /docs for the UI."}

@app.post("/ingest")
async def ingest_repo(request: RepoRequest):
    """
    Endpoint to receive a GitHub URL, clone it, and extract the code.
    """
    repo_url = request.repo_url
    
    if not repo_url.startswith("https://github.com/"):
        raise HTTPException(status_code=400, detail="Please provide a valid GitHub URL.")

    try:
        documents = clone_and_parse_repo(repo_url)
        
        if not documents:
            raise HTTPException(status_code=404, detail="No readable code files found in the repository.")

        total_chunks = vector_store_docs(documents, repo_url)

        return {
            "status": "success", 
            "message": f"Successfully cloned and parsed {len(documents)} files from {repo_url}.",
            "files_read": len(documents),
            "vector_chunks_stored": total_chunks
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process repository: {str(e)}")

@app.post("/chat")
async def chat_with_repo(request: ChatRequest):
    """
    Endpoint to receive a user question and return an AI-generated answer based on the repo.
    """
    user_query = request.query
    
    if not user_query:
         raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    # Placeholder response
    dummy_answer = f"This is a placeholder response for: '{user_query}'"
    
    return {"query": user_query, "answer": dummy_answer}
