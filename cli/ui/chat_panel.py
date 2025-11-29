"""
Rich UI chat panel for DEVO CLI.

Displays agent conversations and execution events in a beautiful terminal interface.
"""
from typing import Optional, Dict, Any
from datetime import datetime
from rich.console import Console, Group
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.live import Live
from rich.layout import Layout


class ChatPanel:
    """Interactive chat panel for displaying agent execution."""

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.messages: list[Dict[str, Any]] = []
        self.current_agent: Optional[str] = None
        self.current_status: str = "Idle"
        self.layout = Layout()
        self.streaming_content: str = ""
        self.streaming_live: Optional[Live] = None

    def _create_message_panel(
        self,
        title: str,
        content: str,
        style: str = "blue",
        border_style: str = "blue",
    ) -> Panel:
        """Create a styled message panel."""
        return Panel(
            content,
            title=f"[bold {style}]{title}[/bold {style}]",
            border_style=border_style,
            padding=(0, 1),
        )

    def _format_timestamp(self, timestamp: Optional[str] = None) -> str:
        """Format timestamp for display."""
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                return dt.strftime("%H:%M:%S")
            except:
                return timestamp
        return datetime.now().strftime("%H:%M:%S")

    def render_user_message(self, content: str) -> None:
        """Render user message."""
        panel = self._create_message_panel(
            title="You",
            content=content,
            style="green",
            border_style="green",
        )
        self.console.print(panel)
        self.console.print()

    def render_agent_start(self, event: Dict[str, Any]) -> None:
        """Render agent start event."""
        agent = event.get("agent", "Agent")
        self.current_agent = agent

        panel = Panel(
            f"[bold cyan]{agent}[/bold cyan] is starting work...",
            border_style="cyan",
            padding=(0, 1),
        )
        self.console.print(panel)

    def render_thinking(self, event: Dict[str, Any]) -> None:
        """Render thinking (for reasoning models like DeepSeek-R1)."""
        content = event.get("content", "")

        if content:
            panel = self._create_message_panel(
                title=f"{self.current_agent or 'Agent'} (Thinking)",
                content=f"[dim italic]{content}[/dim italic]",
                style="yellow",
                border_style="yellow",
            )
            self.console.print(panel)

    def render_content(self, event: Dict[str, Any]) -> None:
        """Render agent content/response."""
        content = event.get("content", "")

        if content:
            # Try to render as markdown
            try:
                md = Markdown(content)
                panel = Panel(
                    md,
                    title=f"[bold blue]{self.current_agent or 'Agent'}[/bold blue]",
                    border_style="blue",
                    padding=(0, 1),
                )
            except:
                panel = self._create_message_panel(
                    title=self.current_agent or "Agent",
                    content=content,
                    style="blue",
                    border_style="blue",
                )

            self.console.print(panel)

    def render_content_chunk(self, event: Dict[str, Any]) -> None:
        """Render streaming content chunk in real-time."""
        # Try different field names for the chunk content
        chunk = event.get("chunk") or event.get("content") or event.get("text") or ""

        if not chunk:
            # No content to display
            return

        if not self.streaming_live:
            # Start streaming display
            self.streaming_content = ""
            self.streaming_live = Live(
                self._create_streaming_panel(),
                console=self.console,
                auto_refresh=False
            )
            self.streaming_live.start()

        # Append chunk - stream word by word for real-time feel
        self.streaming_content += chunk

        # Update display
        self.streaming_live.update(self._create_streaming_panel())
        self.streaming_live.refresh()

    def render_stream_complete(self, event: Dict[str, Any]) -> None:
        """Complete the streaming display."""
        if self.streaming_live:
            # Stop and clear the live display
            self.streaming_live.stop()
            self.streaming_live = None

            # Show final formatted content
            if self.streaming_content:
                try:
                    md = Markdown(self.streaming_content)
                    panel = Panel(
                        md,
                        title=f"[bold blue]{self.current_agent or 'Agent'}[/bold blue]",
                        border_style="blue",
                        padding=(0, 1),
                    )
                except:
                    panel = self._create_message_panel(
                        title=self.current_agent or "Agent",
                        content=self.streaming_content,
                        style="blue",
                        border_style="blue",
                    )

                self.console.print(panel)
                self.streaming_content = ""

    def _create_streaming_panel(self) -> Panel:
        """Create panel for streaming content."""
        content = self.streaming_content if self.streaming_content else "[dim]Generating...[/dim]"

        return Panel(
            Text(content),
            title=f"[bold blue]{self.current_agent or 'Agent'}[/bold blue] [dim](streaming...)[/dim]",
            border_style="cyan",
            padding=(0, 1),
        )

    def render_tool_call_start(self, event: Dict[str, Any]) -> None:
        """Render tool call start."""
        tool = event.get("tool", "unknown")
        args = event.get("arguments", {})

        # Create a formatted view of the tool call
        content = f"[bold cyan]Tool:[/bold cyan] {tool}\n"

        if args:
            content += "\n[bold cyan]Arguments:[/bold cyan]\n"
            for key, value in args.items():
                # Truncate long values
                value_str = str(value)
                if len(value_str) > 100:
                    value_str = value_str[:97] + "..."
                content += f"  [dim]{key}:[/dim] {value_str}\n"

        panel = Panel(
            content,
            title="[bold yellow]🔧 Tool Execution[/bold yellow]",
            border_style="yellow",
            padding=(0, 1),
        )
        self.console.print(panel)

    def render_tool_call_result(self, event: Dict[str, Any]) -> None:
        """Render tool call result."""
        success = event.get("success", False)
        result = event.get("result", {})
        tool = event.get("tool", "unknown")

        if success:
            # Show brief success message
            if isinstance(result, dict):
                if "file_path" in result:
                    msg = f"[green]✓[/green] {tool}: {result.get('file_path')}"
                elif "task_id" in result:
                    msg = f"[green]✓[/green] {tool}: Created task"
                else:
                    msg = f"[green]✓[/green] {tool}: Success"
            else:
                msg = f"[green]✓[/green] {tool}: Success"

            self.console.print(msg)
        else:
            error = event.get("error", "Unknown error")
            panel = Panel(
                f"[red]{error}[/red]",
                title="[bold red]❌ Tool Error[/bold red]",
                border_style="red",
                padding=(0, 1),
            )
            self.console.print(panel)

    def render_file_created(self, event: Dict[str, Any]) -> None:
        """Render file created event."""
        path = event.get("path", "unknown")
        self.console.print(f"[green]📄 Created:[/green] {path}")

    def render_file_modified(self, event: Dict[str, Any]) -> None:
        """Render file modified event."""
        path = event.get("path", "unknown")
        self.console.print(f"[yellow]📝 Modified:[/yellow] {path}")

    def render_user_input_required(self, event: Dict[str, Any]) -> None:
        """Render user input required event."""
        question = event.get("question", "")
        options = event.get("options", [])

        content = f"[bold yellow]Question:[/bold yellow] {question}\n"

        if options:
            content += "\n[bold yellow]Options:[/bold yellow]\n"
            for i, option in enumerate(options, 1):
                content += f"  {i}. {option}\n"

        panel = Panel(
            content,
            title="[bold yellow]❓ User Input Required[/bold yellow]",
            border_style="yellow",
            padding=(0, 1),
        )
        self.console.print(panel)

    def render_task_completed(self, event: Dict[str, Any]) -> None:
        """Render task completed event."""
        task_id = event.get("task_id", "")
        summary = event.get("summary", "")
        deliverables = event.get("deliverables", [])

        content = f"[bold green]Summary:[/bold green] {summary}\n"

        if deliverables:
            content += "\n[bold green]Deliverables:[/bold green]\n"
            for item in deliverables:
                content += f"  • {item}\n"

        panel = Panel(
            content,
            title="[bold green]✅ Task Completed[/bold green]",
            border_style="green",
            padding=(0, 1),
        )
        self.console.print(panel)

    def render_error(self, event: Dict[str, Any]) -> None:
        """Render error event."""
        error = event.get("error", "Unknown error")
        recoverable = event.get("recoverable", False)

        status = "Recoverable" if recoverable else "Fatal"
        content = f"[bold red]Error:[/bold red] {error}\n"
        content += f"[bold red]Status:[/bold red] {status}"

        panel = Panel(
            content,
            title="[bold red]❌ Error[/bold red]",
            border_style="red",
            padding=(0, 1),
        )
        self.console.print(panel)

    def render_done(self, event: Dict[str, Any]) -> None:
        """Render done event."""
        panel = Panel(
            "[bold green]Execution complete![/bold green]",
            border_style="green",
            padding=(0, 1),
        )
        self.console.print(panel)

    def render_connected(self, event: Dict[str, Any]) -> None:
        """Render connected event."""
        panel = Panel(
            "Orchestrator is starting work...",
            border_style="cyan",
            padding=(0, 1),
        )
        self.console.print(panel)

    def render_iteration_start(self, event: Dict[str, Any]) -> None:
        """Render iteration start - silent event."""
        # Silent - just orchestrator internal state
        pass

    def render_context_assembled(self, event: Dict[str, Any]) -> None:
        """Render context assembled - silent event."""
        # Silent - just orchestrator internal state
        pass

    def render_event(self, event: Dict[str, Any]) -> None:
        """Render event based on type."""
        event_type = event.get("type", "unknown")

        handlers = {
            "agent_start": self.render_agent_start,
            "thinking": self.render_thinking,
            "content": self.render_content,
            "content_chunk": self.render_content_chunk,
            "stream_complete": self.render_stream_complete,
            "tool_call_start": self.render_tool_call_start,
            "tool_call_result": self.render_tool_call_result,
            "file_created": self.render_file_created,
            "file_modified": self.render_file_modified,
            "user_input_required": self.render_user_input_required,
            "task_completed": self.render_task_completed,
            "error": self.render_error,
            "done": self.render_done,
            "connected": self.render_connected,
            "iteration_start": self.render_iteration_start,
            "context_assembled": self.render_context_assembled,
        }

        handler = handlers.get(event_type)
        if handler:
            handler(event)
        else:
            # Silent for unknown internal orchestrator events
            # Only show if it looks like something important
            if event_type not in ["ping", "pong", "heartbeat", "status_update"]:
                self.console.print(f"[dim]Debug: {event_type}[/dim]")

    def get_input(self, prompt: str = "> ") -> str:
        """Get user input."""
        return self.console.input(f"[bold green]{prompt}[/bold green]")

    def show_spinner(self, text: str = "Processing...") -> Progress:
        """Show spinner with text."""
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        )
        progress.add_task(description=text, total=None)
        return progress
