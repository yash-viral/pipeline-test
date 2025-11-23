from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, UUID
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.sql import func
from database_config import Base
import uuid

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_name = Column(String)
    agent_name_constant = Column(String)
    agent_description = Column(Text)
    agent_category_id = Column(Integer)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now())

class Repository(Base):
    __tablename__ = "repositories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"))
    repo_for = Column(String, nullable=False)
    repository_url = Column(String, nullable=False)
    repository_type = Column(String, default='git')
    repository_branch = Column(String, default='main')
    docker_registry_url = Column(String)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now())