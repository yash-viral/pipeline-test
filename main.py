from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.github_build_routes import router as github_build_router
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Pipeline Test - GitHub Build Service", 
    version="1.0.0",
    description="Agent-based Docker image build service"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(github_build_router, prefix="/api/github-build")

@app.get("/")
async def root():
    return {
        "service": "Pipeline Test - GitHub Build Service",
        "version": "1.0.0",
        "endpoints": {
            "list_agents": "GET /api/github-build/agents",
            "build_agent": "POST /api/github-build/build/agent",
            "build_multiple_agents": "POST /api/github-build/build/agents",
            "get_agent_repo": "GET /api/github-build/agent/{agent_name}/repository",
            "list_repos": "GET /api/github-build/repositories"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)