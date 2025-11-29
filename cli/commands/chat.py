"""
Interactive chat session for DEVO CLI.

Handles the chat interface with agent execution streaming.
"""
import asyncio
import signal
import sys
from typing import Optional, Dict, Any
from rich.console import Console
from rich.prompt import Prompt

from ..client import APIClient, APIError, WebSocketClient
from ..ui import ChatPanel, StatusPanel
from ..config import config


class ChatSession:
    """Interactive chat session with agent execution."""

    def __init__(self, project_id: str, console: Optional[Console] = None):
        self.project_id = project_id
        self.console = console or Console()
        self.chat_panel = ChatPanel(self.console)
        self.status_panel = StatusPanel(self.console)
        self.api_client: Optional[APIClient] = None
        self.ws_client: Optional[WebSocketClient] = None
        self.paused = False
        self.waiting_for_input = False
        self.current_question: Optional[str] = None
        self.interrupt_requested = False
        self.execution_active = False

    def setup_interrupt_handler(self):
        """Setup Ctrl+C handler."""
        def signal_handler(sig, frame):
            if self.execution_active:
                # Set flag and cancel via WebSocket
                self.interrupt_requested = True
                self.console.print("\n[yellow]Interrupt received - cancelling task...[/yellow]")
                if self.ws_client and self.ws_client.connection:
                    try:
                        asyncio.create_task(self.ws_client.cancel_execution())
                    except:
                        pass
            else:
                # Not executing, just exit
                self.console.print("\n[yellow]Goodbye![/yellow]")
                sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

    def handle_interrupt(self):
        """Handle interrupt after execution completes."""
        if not self.interrupt_requested:
            return

        self.console.print("\n[bold yellow]Task cancelled by user[/bold yellow]\n")
        self.interrupt_requested = False

    def pause_and_ask(self):
        """Pause execution and ask user question."""
        self.paused = True
        self.console.print("\n[cyan]Execution paused[/cyan]\n")

        question = Prompt.ask("Ask a question")

        # For now, just show the question and resume
        # In a full implementation, this would send to the appropriate agent
        self.console.print(f"\n[dim]Question noted: {question}[/dim]\n")
        self.console.print("[cyan]Resuming execution...[/cyan]\n")
        self.paused = False

    def cancel_task(self):
        """Cancel current task."""
        self.console.print("\n[yellow]Cancelling current task...[/yellow]\n")

        # Send cancel via WebSocket if connected
        if self.ws_client and self.ws_client.connection:
            asyncio.create_task(self.ws_client.cancel_execution())

        sys.exit(0)

    def save_and_exit(self):
        """Save checkpoint and exit."""
        self.console.print("\n[cyan]Saving checkpoint and exiting...[/cyan]\n")

        # In a full implementation, this would create a checkpoint
        # For now, just exit gracefully
        sys.exit(0)

    async def start(self):
        """Start chat session."""
        # Setup interrupt handler
        self.setup_interrupt_handler()

        try:
            # Initialize API client
            self.api_client = APIClient()
            await self.api_client.__aenter__()

            # Get project info
            try:
                project = await self.api_client.get_project(self.project_id)
            except APIError as e:
                self.status_panel.show_error(f"Project not found: {e.message}")
                return

            # Show welcome
            self.status_panel.show_welcome(project.get("name"))

            # Show brief status
            agents = await self.api_client.get_project_agents(self.project_id)
            tasks = await self.api_client.list_tasks(self.project_id, status="in_progress")

            self.console.print(f"[dim]Agents: {len(agents)} | Tasks in progress: {len(tasks)}[/dim]\n")

            # Main chat loop
            await self.chat_loop()

        except Exception as e:
            self.status_panel.show_error(f"Error: {str(e)}")
        finally:
            # Cleanup
            if self.api_client:
                await self.api_client.__aexit__(None, None, None)

    async def chat_loop(self):
        """Main chat loop."""
        while True:
            # Get user input
            self.console.print()
            user_message = self.chat_panel.get_input("You: ")

            if not user_message.strip():
                continue

            # Check for special commands
            if user_message.lower() in ["/exit", "/quit", "/q"]:
                self.console.print("[cyan]Goodbye![/cyan]")
                break

            if user_message.lower() == "/status":
                await self.show_status()
                continue

            if user_message.lower() == "/agents":
                await self.show_agents()
                continue

            if user_message.lower() == "/help":
                self.show_help()
                continue

            # Execute with agents
            await self.execute_message(user_message)

    async def execute_message(self, message: str):
        """Execute user message with agents."""
        # Render user message
        self.chat_panel.render_user_message(message)
        self.console.print()

        self.execution_active = True
        self.interrupt_requested = False

        try:
            # Initialize WebSocket client
            self.ws_client = WebSocketClient()

            # Execute and stream events
            async for event in self.ws_client.execute_project(
                project_id=self.project_id,
                message=message,
            ):
                # Check for interrupt
                if self.interrupt_requested:
                    break

                # Render event
                self.chat_panel.render_event(event)

                # Handle user input requests
                if event.get("type") == "user_input_required":
                    await self.handle_user_input_request(event)

        except Exception as e:
            if not self.interrupt_requested:
                self.status_panel.show_error(f"Execution error: {str(e)}")

        finally:
            self.execution_active = False
            self.ws_client = None
            self.handle_interrupt()

    async def handle_user_input_request(self, event: Dict[str, Any]):
        """Handle user input request from agent."""
        self.waiting_for_input = True

        question = event.get("question", "Please provide input")
        options = event.get("options", [])

        # Get user response
        if options:
            # Show as choices
            choices = [str(i) for i in range(1, len(options) + 1)]
            response_idx = Prompt.ask(
                "Your answer",
                choices=choices + ["other"],
                default="1"
            )

            if response_idx == "other":
                response = Prompt.ask("Enter your answer")
            else:
                response = options[int(response_idx) - 1]
        else:
            response = Prompt.ask("Your answer")

        # Send response via WebSocket
        if self.ws_client:
            await self.ws_client.send_user_input(response)

        self.waiting_for_input = False

    async def show_status(self):
        """Show project status."""
        if not self.api_client:
            return

        try:
            project = await self.api_client.get_project(self.project_id)
            agents = await self.api_client.get_project_agents(self.project_id)
            tasks = await self.api_client.list_tasks(self.project_id)

            self.status_panel.render_full_status(project, agents, tasks)

        except APIError as e:
            self.status_panel.show_error(f"Failed to get status: {e.message}")

    async def show_agents(self):
        """Show project agents."""
        if not self.api_client:
            return

        try:
            agents = await self.api_client.get_project_agents(self.project_id)

            if not agents:
                self.status_panel.show_info("No agents in this project yet")
                return

            table = self.status_panel.render_agents_table(agents)
            self.console.print(table)

        except APIError as e:
            self.status_panel.show_error(f"Failed to list agents: {e.message}")

    def show_help(self):
        """Show help message."""
        help_text = """
[bold cyan]DEVO Chat Commands[/bold cyan]

[bold]Special Commands:[/bold]
  /exit, /quit, /q  - Exit chat session
  /status           - Show project status
  /agents           - Show active agents
  /help             - Show this help message

[bold]Interrupt:[/bold]
  Ctrl+C            - Pause execution and show options

[bold]Usage:[/bold]
Just type your request and press Enter. The agents will work together
to accomplish your task.

[bold]Examples:[/bold]
  Add user authentication with JWT
  Create a REST API for blog posts
  Write tests for the User model
  Refactor the authentication code
        """

        self.console.print(help_text)
