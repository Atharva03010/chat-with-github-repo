from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.github_ingestor import clone_and_parse_repo
from services.vector_store import vector_store_docs
from services.rag import get_answers

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
async def serve_frontend():
    """Serve the frontend HTML file."""
    return FileResponse("static/index.html")

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
  
    try:
        # Query the RAG pipeline
        result = get_answers(user_query)
        
        return {
            "query": user_query, 
            "answer": result["answer"],
            "referenced_files": list(set(result["sources"])) # Remove duplicates
        }
    except ValueError as ve:
        # Catch the error if the database doesn't exist yet
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")
