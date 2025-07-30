"""
Execution context management for Brain agents.

This module provides utilities for capturing, propagating, and managing
execution context across agent boundaries in the Brain multi-agent system.
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import Request
from .types import WorkflowContext


class ExecutionContext:
    """
    Captures and manages execution context for Brain agent operations.
    
    This class handles workflow tracking, session management, and context
    propagation across agent boundaries to enable proper DAG building
    and audit trails.
    """
    
    def __init__(
        self,
        workflow_id: str,
        session_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        parent_workflow_id: Optional[str] = None,
        root_workflow_id: Optional[str] = None,
        workflow_name: Optional[str] = None,
        workflow_tags: Optional[list] = None,
        brain_request_id: Optional[str] = None,
        execution_id: Optional[str] = None,
        agent_node_id: Optional[str] = None,
    ):
        self.workflow_id = workflow_id
        self.session_id = session_id
        self.actor_id = actor_id
        self.parent_workflow_id = parent_workflow_id
        self.root_workflow_id = root_workflow_id or workflow_id
        self.workflow_name = workflow_name
        self.workflow_tags = workflow_tags or []
        self.brain_request_id = brain_request_id
        self.execution_id = execution_id
        self.agent_node_id = agent_node_id
    
    @classmethod
    def from_request(cls, request: Request, agent_node_id: Optional[str] = None) -> "ExecutionContext":
        """
        Extract execution context from FastAPI request headers.
        
        Args:
            request: FastAPI Request object
            agent_node_id: Current agent node ID
            
        Returns:
            ExecutionContext instance with extracted context
        """
        headers = request.headers
        
        workflow_id = headers.get("x-workflow-id")
        if not workflow_id:
            # Generate new workflow ID if none provided
            workflow_id = cls._generate_workflow_id()
        
        workflow_tags = []
        workflow_tags_header = headers.get("x-workflow-tags")
        if workflow_tags_header:
            workflow_tags = [tag.strip() for tag in workflow_tags_header.split(",")]
        
        return cls(
            workflow_id=workflow_id,
            session_id=headers.get("x-session-id"),
            actor_id=headers.get("x-actor-id"),
            parent_workflow_id=headers.get("x-parent-workflow-id"),
            root_workflow_id=headers.get("x-root-workflow-id"),
            workflow_name=headers.get("x-workflow-name"),
            workflow_tags=workflow_tags,
            brain_request_id=headers.get("x-brain-request-id"),
            execution_id=headers.get("x-execution-id"),
            agent_node_id=agent_node_id,
        )
    
    @classmethod
    def create_new(
        cls,
        agent_node_id: str,
        session_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        workflow_name: Optional[str] = None,
        workflow_tags: Optional[list] = None,
    ) -> "ExecutionContext":
        """
        Create a new execution context for starting a workflow.
        
        Args:
            agent_node_id: Current agent node ID
            session_id: Optional session ID
            actor_id: Optional actor ID
            workflow_name: Optional workflow name
            workflow_tags: Optional workflow tags
            
        Returns:
            New ExecutionContext instance
        """
        workflow_id = cls._generate_workflow_id()
        
        return cls(
            workflow_id=workflow_id,
            session_id=session_id,
            actor_id=actor_id,
            root_workflow_id=workflow_id,
            workflow_name=workflow_name,
            workflow_tags=workflow_tags or [],
            agent_node_id=agent_node_id,
        )
    
    def create_child_context(self, new_agent_node_id: Optional[str] = None) -> "ExecutionContext":
        """
        Create a child execution context for cross-agent calls.
        
        This maintains the workflow chain while creating a new execution
        context that properly tracks parent-child relationships.
        
        Args:
            new_agent_node_id: Target agent node ID for the call
            
        Returns:
            New ExecutionContext for the child execution
        """
        child_workflow_id = self._generate_workflow_id()
        
        return ExecutionContext(
            workflow_id=child_workflow_id,
            session_id=self.session_id,
            actor_id=self.actor_id,
            parent_workflow_id=self.workflow_id,  # Current becomes parent
            root_workflow_id=self.root_workflow_id,
            workflow_name=self.workflow_name,
            workflow_tags=self.workflow_tags.copy() if self.workflow_tags else [],
            agent_node_id=new_agent_node_id or self.agent_node_id,
        )
    
    def to_workflow_context(self) -> WorkflowContext:
        """
        Convert to WorkflowContext for use with BrainClient.
        
        Returns:
            WorkflowContext instance
        """
        return WorkflowContext(
            workflow_id=self.workflow_id,
            session_id=self.session_id,
            actor_id=self.actor_id,
            parent_workflow_id=self.parent_workflow_id,
            root_workflow_id=self.root_workflow_id,
            workflow_name=self.workflow_name,
            workflow_tags=self.workflow_tags,
        )
    
    def to_headers(self) -> Dict[str, str]:
        """
        Convert execution context to HTTP headers for propagation.
        
        Returns:
            Dictionary of headers for HTTP requests
        """
        headers = {
            "X-Workflow-ID": self.workflow_id,
        }
        
        if self.session_id:
            headers["X-Session-ID"] = self.session_id
        if self.actor_id:
            headers["X-Actor-ID"] = self.actor_id
        if self.parent_workflow_id:
            headers["X-Parent-Workflow-ID"] = self.parent_workflow_id
        if self.root_workflow_id:
            headers["X-Root-Workflow-ID"] = self.root_workflow_id
        if self.workflow_name:
            headers["X-Workflow-Name"] = self.workflow_name
        if self.workflow_tags:
            headers["X-Workflow-Tags"] = ",".join(self.workflow_tags)
        if self.brain_request_id:
            headers["X-Brain-Request-ID"] = self.brain_request_id
        if self.execution_id:
            headers["X-Execution-ID"] = self.execution_id
        if self.agent_node_id:
            headers["X-Agent-Node-ID"] = self.agent_node_id
        
        return headers
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert execution context to dictionary representation.
        
        Returns:
            Dictionary representation of the context
        """
        return {
            "workflow_id": self.workflow_id,
            "session_id": self.session_id,
            "actor_id": self.actor_id,
            "parent_workflow_id": self.parent_workflow_id,
            "root_workflow_id": self.root_workflow_id,
            "workflow_name": self.workflow_name,
            "workflow_tags": self.workflow_tags,
            "brain_request_id": self.brain_request_id,
            "execution_id": self.execution_id,
            "agent_node_id": self.agent_node_id,
        }
    
    @staticmethod
    def _generate_workflow_id() -> str:
        """Generate a unique workflow ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        return f"wf_{timestamp}_{unique_id}"
    
    def __repr__(self) -> str:
        return f"ExecutionContext(workflow_id='{self.workflow_id}', agent_node_id='{self.agent_node_id}')"
