import os
import shutil
import tempfile
from git import Repo

SUPPORTED_EXTENSIONS = {'.py', '.java', '.cpp', '.c', '.js', '.ts', '.md', '.txt', '.html', '.css','.sql'}

# folders that are massive and irrelevant to the core logic
IGNORED_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', 'env', 'build', 'dist', 'target'}

def clone_and_parse_repo(repo_url: str) -> list[dict]:
    """
    Clones a GitHub repository, filters for relevant code files, 
    and returns a list of dictionaries containing file paths and content.
    """
    #temporary directory that the OS will help manage
    temp_dir = tempfile.mkdtemp()
    documents = []

    try:
        print(f"Cloning {repo_url} into temporary directory...")
        Repo.clone_from(repo_url, temp_dir)

        for root, dirs, files in os.walk(temp_dir):
            # modifying the dirs list in-place to prevent os.walk from entering ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                
                if ext in SUPPORTED_EXTENSIONS:
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            rel_path = os.path.relpath(file_path, temp_dir)
                            documents.append({"path": rel_path, "content": content})
                    except Exception as e:
                        print(f"Skipping file {file} due to read error: {e}")

    finally:
        # cleaning up the temporary directory after processing
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    # print(documents)

    return documents