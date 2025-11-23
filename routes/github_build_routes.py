from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database_config import get_db
from services.github_build_service import GitHubBuildService
from pydantic import BaseModel
from typing import List

router = APIRouter(tags=["GitHub Build"])

class AgentBuildRequest(BaseModel):
    agent_name: str

class MultipleAgentBuildRequest(BaseModel):
    agent_names: List[str]

@router.post("/build/agent")
def trigger_agent_build(agent_request: AgentBuildRequest, db: Session = Depends(get_db)):
    """Trigger Docker image build for a specific agent"""
    try:
        service = GitHubBuildService(db)
        return service.trigger_agent_build(agent_request.agent_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger agent build: {str(e)}")

@router.get("/agent/{agent_name}/repository")
def get_agent_repository(agent_name: str, db: Session = Depends(get_db)):
    """Get repository info for a specific agent"""
    try:
        service = GitHubBuildService(db)
        repo_info = service.get_agent_repository(agent_name)
        if not repo_info:
            raise HTTPException(status_code=404, detail="Agent or repository not found")
        return repo_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch agent repository: {str(e)}")

@router.get("/agents")
def get_all_agents(db: Session = Depends(get_db)):
    """Get list of all agents"""
    try:
        service = GitHubBuildService(db)
        return service.get_all_agents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch agents: {str(e)}")

@router.post("/build/agents")
def trigger_multiple_agent_builds(request: MultipleAgentBuildRequest, db: Session = Depends(get_db)):
    """Trigger Docker image builds for multiple agents"""
    try:
        service = GitHubBuildService(db)
        return service.trigger_multiple_agent_builds(request.agent_names)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger multiple agent builds: {str(e)}")

@router.get("/repositories")
def get_repositories_with_releases():
    """Get all organization repositories with their latest release info"""
    try:
        service = GitHubBuildService()
        return service.get_repositories_with_releases()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repositories: {str(e)}")