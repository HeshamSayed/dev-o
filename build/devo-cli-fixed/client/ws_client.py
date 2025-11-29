"""
WebSocket client for real-time agent execution streaming.

Handles WebSocket connections to receive agent execution events.
"""
import asyncio
import json
from typing import Optional, Dict, Any, AsyncGenerator, Callable
from urllib.parse import urlparse, urlunparse
import websockets
from websockets.exceptions import WebSocketException
from rich.console import Console

from ..config import config

console = Console()


class WebSocketClient:
    """Client for WebSocket communication with DEVO backend."""

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self.api_url = api_url or config.get_api_url()
        self.api_key = api_key or config.get_api_key()
        self.ws_url = self._get_ws_url()
        self.connection: Optional[websockets.WebSocketClientProtocol] = None

    def _get_ws_url(self) -> str:
        """Convert HTTP URL to WebSocket URL."""
        parsed = urlparse(self.api_url)

        # Replace http/https with ws/wss
        scheme = "wss" if parsed.scheme == "https" else "ws"

        return urlunparse((
            scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        ))

    async def connect(self, path: str) -> None:
        """Connect to WebSocket endpoint."""
        url = f"{self.ws_url}{path}"

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            self.connection = await websockets.connect(
                url,
                extra_headers=headers,
                ping_interval=20,
                ping_timeout=10,
            )
        except Exception as e:
            console.print(f"[red]Failed to connect to WebSocket: {e}[/red]")
            raise

    async def disconnect(self) -> None:
        """Disconnect from WebSocket."""
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def send(self, data: Dict[str, Any]) -> None:
        """Send message to WebSocket."""
        if not self.connection:
            raise RuntimeError("WebSocket not connected")

        await self.connection.send(json.dumps(data))

    async def receive(self) -> Dict[str, Any]:
        """Receive message from WebSocket."""
        if not self.connection:
            raise RuntimeError("WebSocket not connected")

        message = await self.connection.recv()
        return json.loads(message)

    async def stream_events(
        self,
        on_event: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream events from WebSocket.

        Args:
            on_event: Optional callback for each event

        Yields:
            Event dictionaries
        """
        if not self.connection:
            raise RuntimeError("WebSocket not connected")

        try:
            async for message in self.connection:
                event = json.loads(message)

                if on_event:
                    on_event(event)

                yield event

                # Stop if we receive 'done' event
                if event.get("type") == "done":
                    break

        except WebSocketException as e:
            console.print(f"[red]WebSocket error: {e}[/red]")
            raise
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            raise

    async def execute_project(
        self,
        project_id: str,
        message: str,
        on_event: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute project with user message and stream events.

        Args:
            project_id: Project ID
            message: User message
            on_event: Optional callback for each event

        Yields:
            Event dictionaries
        """
        # Connect to project execution WebSocket
        await self.connect(f"/ws/projects/{project_id}/stream/")

        try:
            # Send the user message
            await self.send({
                "type": "user_message",
                "content": message,
            })

            # Stream events
            async for event in self.stream_events(on_event=on_event):
                yield event

        finally:
            await self.disconnect()

    async def execute_agent(
        self,
        agent_id: str,
        task_id: str,
        on_event: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute agent task and stream events.

        Args:
            agent_id: Agent ID
            task_id: Task ID
            on_event: Optional callback for each event

        Yields:
            Event dictionaries
        """
        # Connect to agent execution WebSocket
        await self.connect(f"/ws/agents/{agent_id}/execute/")

        try:
            # Send task execution request
            await self.send({
                "type": "execute_task",
                "task_id": task_id,
            })

            # Stream events
            async for event in self.stream_events(on_event=on_event):
                yield event

        finally:
            await self.disconnect()

    async def send_user_input(self, response: str) -> None:
        """Send user input in response to agent question.

        Args:
            response: User's response
        """
        if not self.connection:
            raise RuntimeError("WebSocket not connected")

        await self.send({
            "type": "user_input",
            "content": response,
        })

    async def cancel_execution(self) -> None:
        """Cancel current execution."""
        if not self.connection:
            raise RuntimeError("WebSocket not connected")

        await self.send({
            "type": "cancel",
        })
