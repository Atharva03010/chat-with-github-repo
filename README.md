# Chat with Repo API

A FastAPI-based application that allows you to ingest GitHub repositories and query them using Retrieval-Augmented Generation (RAG) with AI-powered responses.

## Features

- **Repository Ingestion**: Clone and parse GitHub repositories, extracting code from supported file types (Python, Java, C++, JavaScript, TypeScript, Markdown, HTML, CSS, etc.).
- **Vector Storage**: Chunk code into manageable pieces and store them in a ChromaDB vector database for efficient retrieval.
- **AI-Powered Chat**: Query the ingested repository using natural language and get AI-generated answers based on the code context.
- **FastAPI Backend**: RESTful API with automatic documentation at `/docs`.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/chatwithrepo.git
   cd chatwithrepo
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv1
   source venv1/bin/activate  # On Windows: venv1\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

1. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API documentation**:
   Open your browser and go to `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

### API Endpoints

- **GET /**: Health check endpoint.
- **POST /ingest**: Ingest a GitHub repository.
  - Request body: `{"repo_url": "https://github.com/username/repo"}`
  - Response: Confirmation of ingestion with file count and chunks stored.
- **POST /chat**: Query the repository.
  - Request body: `{"query": "What does this function do?"}`
  - Response: AI-generated answer with referenced files.

## Requirements

- Python 3.8+
- Git
- Google API Key (for Gemini AI)

## Dependencies

- check the requirements.txt

