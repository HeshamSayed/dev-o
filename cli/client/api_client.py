"""
API client for DEVO backend.

Handles HTTP requests to the Django backend API.
"""
import asyncio
from typing import Optional, Dict, Any, List
import httpx
from rich.console import Console

from ..config import config

console = Console()


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(self, status_code: int, message: str, details: Optional[Dict] = None):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class APIClient:
    """Client for communicating with DEVO backend API."""

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self.api_url = api_url or config.get_api_url()
        self.api_key = api_key or config.get_api_key()
        self.client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        self.client = httpx.AsyncClient(
            base_url=self.api_url,
            headers=headers,
            timeout=httpx.Timeout(30.0, connect=10.0),
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        json: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to API."""
        if not self.client:
            raise RuntimeError("APIClient must be used as async context manager")

        try:
            response = await self.client.request(
                method=method,
                url=path,
                json=json,
                params=params,
            )

            # Handle non-JSON responses
            try:
                data = response.json()
            except Exception:
                data = {"detail": response.text}

            if response.is_error:
                raise APIError(
                    status_code=response.status_code,
                    message=data.get("detail", "API request failed"),
                    details=data,
                )

            return data

        except httpx.ConnectError:
            raise APIError(
                status_code=0,
                message=f"Failed to connect to API at {self.api_url}. Is the backend running?",
            )
        except httpx.TimeoutException:
            raise APIError(
                status_code=0,
                message="API request timed out",
            )

    # Auth endpoints
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login user and get JWT token."""
        return await self._request("POST", "/api/auth/login/", json={
            "email": email,
            "password": password,
        })

    async def register(self, email: str, password: str, username: str) -> Dict[str, Any]:
        """Register new user."""
        return await self._request("POST", "/api/auth/register/", json={
            "email": email,
            "password": password,
            "username": username,
        })

    async def get_me(self) -> Dict[str, Any]:
        """Get current user profile."""
        return await self._request("GET", "/api/auth/me/")

    # Project endpoints
    async def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects."""
        return await self._request("GET", "/api/projects/")

    async def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        manifest: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Create new project."""
        return await self._request("POST", "/api/projects/", json={
            "name": name,
            "description": description,
            "manifest": manifest or {},
        })

    async def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details."""
        return await self._request("GET", f"/api/projects/{project_id}/")

    async def update_project(
        self,
        project_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update project."""
        return await self._request("PATCH", f"/api/projects/{project_id}/", json=kwargs)

    async def delete_project(self, project_id: str) -> None:
        """Delete project."""
        await self._request("DELETE", f"/api/projects/{project_id}/")

    async def get_project_status(self, project_id: str) -> Dict[str, Any]:
        """Get project status."""
        return await self._request("GET", f"/api/projects/{project_id}/status/")

    # Agent endpoints
    async def list_agent_types(self) -> List[Dict[str, Any]]:
        """List available agent types."""
        return await self._request("GET", "/api/agent-types/")

    async def get_project_agents(self, project_id: str) -> List[Dict[str, Any]]:
        """List agents in project."""
        return await self._request("GET", f"/api/projects/{project_id}/agents/")

    async def hire_agent(
        self,
        project_id: str,
        agent_type: str,
        custom_instructions: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Hire new agent."""
        return await self._request("POST", f"/api/projects/{project_id}/agents/hire/", json={
            "agent_type": agent_type,
            "custom_instructions": custom_instructions,
        })

    async def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Get agent details."""
        return await self._request("GET", f"/api/agents/{agent_id}/")

    async def update_agent(self, agent_id: str, **kwargs) -> Dict[str, Any]:
        """Update agent."""
        return await self._request("PATCH", f"/api/agents/{agent_id}/", json=kwargs)

    async def delete_agent(self, agent_id: str) -> None:
        """Remove agent."""
        await self._request("DELETE", f"/api/agents/{agent_id}/")

    async def get_agent_messages(
        self,
        agent_id: str,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Get agent messages."""
        return await self._request("GET", f"/api/agents/{agent_id}/messages/", params={
            "limit": limit,
        })

    async def send_agent_message(
        self,
        agent_id: str,
        content: str,
        message_type: str = "user_message",
    ) -> Dict[str, Any]:
        """Send message to agent."""
        return await self._request("POST", f"/api/agents/{agent_id}/messages/", json={
            "content": content,
            "message_type": message_type,
        })

    # Task endpoints
    async def list_tasks(
        self,
        project_id: str,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List project tasks."""
        params = {}
        if status:
            params["status"] = status

        return await self._request("GET", f"/api/projects/{project_id}/tasks/", params=params)

    async def create_task(
        self,
        project_id: str,
        title: str,
        description: Optional[str] = None,
        task_type: str = "task",
        priority: int = 3,
    ) -> Dict[str, Any]:
        """Create new task."""
        return await self._request("POST", f"/api/projects/{project_id}/tasks/", json={
            "title": title,
            "description": description,
            "task_type": task_type,
            "priority": priority,
        })

    async def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task details."""
        return await self._request("GET", f"/api/tasks/{task_id}/")

    async def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """Update task."""
        return await self._request("PATCH", f"/api/tasks/{task_id}/", json=kwargs)

    # Checkpoint endpoints
    async def list_checkpoints(self, project_id: str) -> List[Dict[str, Any]]:
        """List project checkpoints."""
        return await self._request("GET", f"/api/projects/{project_id}/checkpoints/")

    async def create_checkpoint(
        self,
        project_id: str,
        name: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create project checkpoint."""
        return await self._request("POST", f"/api/projects/{project_id}/checkpoints/", json={
            "name": name,
            "description": description,
        })

    # Health check
    async def health_check(self) -> bool:
        """Check if API is healthy."""
        try:
            await self._request("GET", "/api/health/")
            return True
        except APIError:
            return False
