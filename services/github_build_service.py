import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from database_config import get_db
from postgres_models import Agent, Repository

class GitHubBuildService:
    def __init__(self, db: Session = None):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_org = os.getenv("GITHUB_ORG", "Yash-AI-Technologies")
        if not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.db = db
    
    def get_org_repositories(self) -> List[Dict[str, Any]]:
        """Get all repositories for the organization"""
        repos = []
        page = 1
        
        while True:
            url = f"https://api.github.com/orgs/{self.github_org}/repos"
            params = {'page': page, 'per_page': 100, 'type': 'private'}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            page_repos = response.json()
            
            if not page_repos:
                break
                
            repos.extend(page_repos)
            page += 1
        
        return repos
    
    def get_latest_release(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Get latest release for a repository"""
        url = f"https://api.github.com/repos/{self.github_org}/{repo_name}/releases/latest"
        
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        
        return response.json()
    
    def get_repositories_with_releases(self) -> List[Dict[str, Any]]:
        """Get all repositories with their latest release info"""
        repos = self.get_org_repositories()
        result = []
        
        for repo in repos:
            repo_name = repo['name']
            release = self.get_latest_release(repo_name)
            
            if release:
                result.append({
                    "repo_name": repo_name,
                    "version": release['tag_name'],
                    "zip_url": release['zipball_url'],
                    "branch": release.get('target_commitish', 'main'),
                    "release_name": release.get('name', release['tag_name'])
                })
        
        return result
    
    def trigger_matrix_build_workflow(self, repos_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Trigger GitHub Actions matrix workflow"""
        # Use your personal GitHub account for the workflow
        github_username = os.getenv("GITHUB_USERNAME", "viral-maru")
        repo_name = os.getenv("GITHUB_REPO_NAME", "pipeline-test")
        dispatch_url = f"https://api.github.com/repos/{github_username}/{repo_name}/dispatches"
        
        payload = {
            "event_type": "build-matrix",
            "client_payload": {
                "repos_json": repos_data,
                "max_parallel": 5,
                "timestamp": str(datetime.now())
            }
        }
        
        response = requests.post(dispatch_url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return {
            "status": "triggered", 
            "repo_count": len(repos_data),
            "trigger_type": "repository_dispatch"
        }
    
    def get_agent_repository(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get repository info for an agent by name"""
        if not self.db:
            raise ValueError("Database session required")
        
        agent = self.db.query(Agent).filter(Agent.agent_name == agent_name).first()
        if not agent:
            return None
        
        repository = self.db.query(Repository).filter(Repository.agent_id == agent.id).first()
        if not repository:
            return None
        
        # Extract repo name from URL
        repo_url = repository.repository_url
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        
        return {
            "agent_name": agent_name,
            "repo_name": repo_name,
            "repository_url": repo_url,
            "branch": repository.repository_branch or "dev"
        }
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get all agents from database"""
        if not self.db:
            raise ValueError("Database session required")
        
        agents = self.db.query(Agent).filter(Agent.is_deleted == False).all()
        return [{
            "id": str(agent.id),
            "agent_name": agent.agent_name,
            "agent_description": agent.agent_description
        } for agent in agents]
    
    def trigger_agent_build(self, agent_name: str) -> Dict[str, Any]:
        """Trigger build for a specific agent"""
        agent_repo = self.get_agent_repository(agent_name)
        if not agent_repo:
            raise ValueError(f"No repository found for agent: {agent_name}")
        
        # Get latest release or use dev branch
        release = self.get_latest_release(agent_repo["repo_name"])
        
        if release:
            build_data = {
                "repo_name": agent_repo["repo_name"],
                "version": release['tag_name'],
                "zip_url": release['zipball_url'],
                "has_release": True
            }
        else:
            build_data = {
                "repo_name": agent_repo["repo_name"],
                "version": "dev",
                "branch": agent_repo["branch"],
                "has_release": False
            }
        
        return self.trigger_matrix_build_workflow([build_data])
    
    def trigger_multiple_agent_builds(self, agent_names: List[str]) -> Dict[str, Any]:
        """Trigger builds for multiple agents"""
        build_data_list = []
        
        for agent_name in agent_names:
            agent_repo = self.get_agent_repository(agent_name)
            if not agent_repo:
                continue
            
            release = self.get_latest_release(agent_repo["repo_name"])
            
            if release:
                build_data = {
                    "repo_name": agent_repo["repo_name"],
                    "version": release['tag_name'],
                    "zip_url": release['zipball_url'],
                    "has_release": True
                }
            else:
                build_data = {
                    "repo_name": agent_repo["repo_name"],
                    "version": "dev",
                    "branch": agent_repo["branch"],
                    "has_release": False
                }
            
            build_data_list.append(build_data)
        
        if not build_data_list:
            raise ValueError("No valid repositories found for provided agents")
        
        return self.trigger_matrix_build_workflow(build_data_list)