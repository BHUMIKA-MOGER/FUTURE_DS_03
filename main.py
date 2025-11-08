from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
from github import Github
from langchain_community.llms import Ollama # For talking to your local Mistral model
import os
import json

# --- 1. CONFIGURATION ---

# Load environment variables (secrets) from the .env file
load_dotenv()

# Get tokens and URLs from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables.")

# Initialize the GitHub client
g = Github(GITHUB_TOKEN)

# Initialize the FastAPI application
app = FastAPI()

# --- 2. CORE LOGIC FUNCTIONS ---

async def get_pr_diff(repo_full_name: str, pr_number: int) -> str:
    """Fetches the code changes (diff/patch) from the pull request."""
    try:
        repo = g.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)

        full_diff = ""
        
        # Iterate over files changed in the PR
        for file in pr.get_files():
            # Only process files that have a patch (code changes)
            if file.patch:
                full_diff += f"--- FILE: {file.filename} ---\n"
                full_diff += file.patch # The diff content (lines starting with + or -)
                full_diff += "\n\n"
        
        return full_diff

    except Exception as e:
        print(f"Error fetching PR diff for {repo_full_name}#{pr_number}: {e}")
        return ""

async def get_ai_review(code_diff: str) -> str:
    """Sends the code diff to the local LLM (Mistral) for review."""
    
    # 1. Define the role for the LLM (Prompt Engineering)
    system_prompt = (
        "You are an expert Python software engineer and security reviewer. "
        "Review the following Git diff for bugs, logical flaws, security vulnerabilities, "
        "and adherence to best practices. Use a clear, bulleted list format. "
        "Provide constructive feedback and suggest specific code improvements. "
        "If the code is flawless, state only: '🤖 Review: LGTM (Looks Good To Me)'. "
        "Keep the review concise, limited to 5-7 points max."
    )
    
    # 2. Prepare the full prompt for Mistral
    full_prompt = f"{system_prompt}\n\nReview this code diff:\n\n{code_diff}"
    
    # 3. Initialize and call the local Ollama LLM
    try:
        # Connects to http://localhost:11434 by default, or uses OLLAMA_BASE_URL if set
        llm = Ollama(model="tinyllama", base_url=OLLAMA_URL)
        
        print("LOG: Sending diff to Mistral for analysis...")
        response = llm.invoke(full_prompt)
        
        return response

    except Exception as e:
        return f"🚨 AI Review Failed: Could not connect to local Ollama server. Error: {e}"

async def post_review_comment(repo_full_name: str, pr_number: int, review_comment: str):
    """Posts the final AI review back to the Pull Request on GitHub."""
    try:
        repo = g.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)
        
        final_comment = (
            "## 🤖 AI Code Review Summary\n\n"
            "*(Powered by local Mistral LLM)*\n\n"
            f"{review_comment}"
        )
        pr.create_issue_comment(final_comment)
        print(f"LOG: Successfully posted review for PR #{pr_number}")
        
    except Exception as e:
        print(f"Error posting comment to GitHub: {e}")

async def process_pull_request_review(repo_full_name: str, pr_number: int):
    """Orchestrates the entire review pipeline."""
    
    # Step 1: Fetch the Diff
    diff = await get_pr_diff(repo_full_name, pr_number)
    
    if not diff:
        # If the diff is empty (e.g., a documentation change with no code), skip review
        return post_review_comment(repo_full_name, pr_number, "No code changes detected to review.")
        
    # Step 2: Get AI Review
    review_comment = await get_ai_review(diff)
    
    # Step 3: Post Comment to GitHub
    await post_review_comment(repo_full_name, pr_number, review_comment)
    
# --- 3. WEBHOOK ENDPOINT ---

@app.post("/webhook")
async def handle_github_webhook(request: Request):
    """Listens for GitHub webhook events on the public ngrok URL."""
    
    event_type = request.headers.get("X-GitHub-Event")
    if not event_type:
        raise HTTPException(status_code=400, detail="Missing X-GitHub-Event header")

    try:
        payload = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Filter for Pull Request events that are opened or updated (synchronize)
    if event_type == "pull_request" and payload.get("action") in ["opened", "synchronize"]:
        
        pr_number = payload["pull_request"]["number"]
        repo_full_name = payload["repository"]["full_name"]
        
        print(f"LOG: Received PR event for {repo_full_name}#{pr_number}. Initiating review...")
        
        # Initiate the core logic without blocking the webhook return
        await process_pull_request_review(repo_full_name, pr_number)
        
        # Return a quick 200 OK response to GitHub
        return {"message": f"Review initiated for PR #{pr_number}"}
    
    return {"message": "Event ignored"}

# --- 4. START SERVER COMMAND ---

if __name__ == "__main__":
    import uvicorn
    # Start the server on port 8000
    print("\n--- Starting AI Code Review Bot ---")
    print(f"GitHub Bot Initialized for user: {g.get_user().login}")
    print("WARNING: Ensure Ollama server is running (http://localhost:11434) and the 'mistral' model is pulled.")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)