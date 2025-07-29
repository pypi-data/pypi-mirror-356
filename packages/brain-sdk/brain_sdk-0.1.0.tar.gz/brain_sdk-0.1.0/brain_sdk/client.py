import requests
from typing import Dict, Any, Optional
import uuid
import datetime
from .types import WorkflowContext, ExecutionMetadata

class BrainClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api/v1"
        self._current_workflow_context: Optional[WorkflowContext] = None
    
    def _generate_id(self, prefix: str) -> str:
        """Generates a unique ID with a given prefix."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        return f"{prefix}_{timestamp}_{unique_id}"

    def _get_headers_with_context(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Combines provided headers with current workflow context headers."""
        if headers is None:
            headers = {}
        
        if self._current_workflow_context:
            context_headers = self._current_workflow_context.to_headers()
            headers.update(context_headers)
        
        return headers

    def register_node(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register agent node with Brain server"""
        response = requests.post(f"{self.api_base}/nodes/register", json=node_data)
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
    
    def update_health(self, node_id: str, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update node health status"""
        response = requests.put(f"{self.api_base}/nodes/{node_id}/health", json=health_data)
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
    
    def get_nodes(self) -> Dict[str, Any]:
        """Get all registered nodes"""
        response = requests.get(f"{self.api_base}/nodes")
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()

    def execute_reasoner(self, reasoner_id: str, input_data: Dict[str, Any], context: Optional[WorkflowContext] = None) -> Dict[str, Any]:
        """
        Executes a reasoner on the Brain server, including workflow tracking.
        If context is provided, it overrides the current client context for this call.
        """
        headers = {}
        if context:
            headers.update(context.to_headers())
        
        # Ensure a workflow ID exists for this request
        if "X-Workflow-ID" not in headers:
            if self._current_workflow_context and self._current_workflow_context.workflow_id:
                headers["X-Workflow-ID"] = self._current_workflow_context.workflow_id
            else:
                headers["X-Workflow-ID"] = self._generate_id("wf")
        
        # Ensure a brain request ID exists for this request
        if "X-Brain-Request-ID" not in headers:
            headers["X-Brain-Request-ID"] = self._generate_id("req")

        # Add other context headers if available in current client context
        headers = self._get_headers_with_context(headers)

        payload = {"input": input_data}
        response = requests.post(f"{self.api_base}/reasoners/{reasoner_id}", json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        # Extract execution metadata from response headers
        execution_metadata = ExecutionMetadata.from_headers(dict(response.headers))
        if execution_metadata:
            result["execution_metadata"] = execution_metadata.to_dict() # Convert dataclass to dict
        
        return result

    def execute_skill(self, skill_id: str, input_data: Dict[str, Any], context: Optional[WorkflowContext] = None) -> Dict[str, Any]:
        """
        Executes a skill on the Brain server, including workflow tracking.
        If context is provided, it overrides the current client context for this call.
        """
        headers = {}
        if context:
            headers.update(context.to_headers())
        
        # Ensure a workflow ID exists for this request
        if "X-Workflow-ID" not in headers:
            if self._current_workflow_context and self._current_workflow_context.workflow_id:
                headers["X-Workflow-ID"] = self._current_workflow_context.workflow_id
            else:
                headers["X-Workflow-ID"] = self._generate_id("wf")
        
        # Ensure a brain request ID exists for this request
        if "X-Brain-Request-ID" not in headers:
            headers["X-Brain-Request-ID"] = self._generate_id("req")

        # Add other context headers if available in current client context
        headers = self._get_headers_with_context(headers)

        payload = {"input": input_data}
        response = requests.post(f"{self.api_base}/skills/{skill_id}", json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        # Extract execution metadata from response headers
        execution_metadata = ExecutionMetadata.from_headers(dict(response.headers))
        if execution_metadata:
            result["execution_metadata"] = execution_metadata.to_dict() # Convert dataclass to dict
        
        return result

    def set_workflow_context(self, context: WorkflowContext):
        """Sets the current workflow context for subsequent calls."""
        self._current_workflow_context = context

    def clear_workflow_context(self):
        """Clears the current workflow context."""
        self._current_workflow_context = None

    def get_workflow_context(self) -> Optional[WorkflowContext]:
        """Returns the current workflow context."""
        return self._current_workflow_context

    async def execute(self, target: str, input_data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Execute a reasoner or skill via the Brain execution gateway.
        
        This method calls the unified execution endpoint that handles both
        reasoners and skills with proper workflow tracking and context propagation.
        
        Args:
            target: Target in format 'node_id.reasoner_name' or 'node_id.skill_name'
            input_data: Input data for the reasoner/skill
            headers: Optional headers to include (will be merged with context headers)
            
        Returns:
            Execution result with metadata
        """
        # Prepare headers with context
        final_headers = {"Content-Type": "application/json"}
        if headers:
            final_headers.update(headers)
        
        # Add workflow context headers if available
        final_headers = self._get_headers_with_context(final_headers)
        
        # Ensure we have a workflow ID
        if "X-Workflow-ID" not in final_headers:
            final_headers["X-Workflow-ID"] = self._generate_id("wf")
        
        # Ensure we have a brain request ID
        if "X-Brain-Request-ID" not in final_headers:
            final_headers["X-Brain-Request-ID"] = self._generate_id("req")
        
        # Prepare payload
        payload = {"input": input_data}
        
        # Make request to execution gateway
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base}/execute/{target}",
                    json=payload,
                    headers=final_headers,
                    timeout=60.0
                )
                response.raise_for_status()
                return response.json()
        except ImportError:
            # Fallback to synchronous requests if httpx not available
            response = requests.post(
                f"{self.api_base}/execute/{target}",
                json=payload,
                headers=final_headers,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()

    def execute_sync(self, target: str, input_data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Synchronous version of execute for compatibility.
        
        Args:
            target: Target in format 'node_id.reasoner_name' or 'node_id.skill_name'
            input_data: Input data for the reasoner/skill
            headers: Optional headers to include
            
        Returns:
            Execution result with metadata
        """
        # Prepare headers with context
        final_headers = {"Content-Type": "application/json"}
        if headers:
            final_headers.update(headers)
        
        # Add workflow context headers if available
        final_headers = self._get_headers_with_context(final_headers)
        
        # Ensure we have a workflow ID
        if "X-Workflow-ID" not in final_headers:
            final_headers["X-Workflow-ID"] = self._generate_id("wf")
        
        # Ensure we have a brain request ID
        if "X-Brain-Request-ID" not in final_headers:
            final_headers["X-Brain-Request-ID"] = self._generate_id("req")
        
        # Prepare payload
        payload = {"input": input_data}
        
        # Make request to execution gateway
        response = requests.post(
            f"{self.api_base}/execute/{target}",
            json=payload,
            headers=final_headers,
            timeout=60.0
        )
        response.raise_for_status()
        return response.json()
