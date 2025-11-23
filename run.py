#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Pipeline Test - GitHub Build Service")
    print("📊 Agent build endpoint: POST /api/github-build/build/agent")
    print("🔍 Agent repository endpoint: GET /api/github-build/agent/{agent_name}/repository")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)