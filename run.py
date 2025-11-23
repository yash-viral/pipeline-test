#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Verify GitHub token is loaded
if not os.getenv("GITHUB_TOKEN"):
    print("❌ GITHUB_TOKEN not found in environment")
    print("Please check your .env file")
    exit(1)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Pipeline Test - GitHub Build Service")
    print("📊 Agent build endpoint: POST /api/github-build/build/agent")
    print("🔍 Agent repository endpoint: GET /api/github-build/agent/{agent_name}/repository")
    print(f"✅ GitHub Token loaded: {os.getenv('GITHUB_TOKEN')[:10]}...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)