"""
Status panel UI components for DEVO CLI.

Displays project status, agent states, and task progress.
"""
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.live import Live


class StatusPanel:
    """Status panel for displaying project and agent information."""

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()

    def render_project_status(self, project: Dict[str, Any]) -> Panel:
        """Render project status panel."""
        name = project.get("name", "Unknown")
        status = project.get("status", "unknown")
        description = project.get("description", "")

        # Status color
        status_colors = {
            "initializing": "yellow",
            "planning": "cyan",
            "in_progress": "blue",
            "completed": "green",
            "error": "red",
        }
        status_color = status_colors.get(status, "white")

        content = f"[bold]Name:[/bold] {name}\n"
        content += f"[bold]Status:[/bold] [{status_color}]{status}[/{status_color}]\n"

        if description:
            content += f"[bold]Description:[/bold] {description}\n"

        # Add statistics if available
        stats = project.get("statistics", {})
        if stats:
            content += f"\n[bold]Statistics:[/bold]\n"
            content += f"  Files: {stats.get('files', 0)}\n"
            content += f"  Lines of Code: {stats.get('loc', 0)}\n"
            content += f"  Tasks: {stats.get('tasks_total', 0)} total | "
            content += f"{stats.get('tasks_completed', 0)} completed\n"

        return Panel(
            content,
            title="[bold cyan]Project Status[/bold cyan]",
            border_style="cyan",
            padding=(0, 1),
        )

    def render_agents_table(self, agents: List[Dict[str, Any]]) -> Table:
        """Render agents table."""
        table = Table(
            title="Active Agents",
            show_header=True,
            header_style="bold magenta",
            border_style="magenta",
        )

        table.add_column("Agent", style="cyan", no_wrap=True)
        table.add_column("Type", style="blue")
        table.add_column("Status", style="yellow")
        table.add_column("Current Task", style="white")

        # Status symbols
        status_symbols = {
            "idle": "⚪",
            "working": "🟢",
            "waiting_input": "🟡",
            "blocked": "🔴",
            "error": "❌",
            "completed": "✅",
        }

        for agent in agents:
            name = agent.get("agent_type", {}).get("name", "Unknown")
            agent_type = agent.get("agent_type", {}).get("role", "unknown")
            status = agent.get("status", "idle")
            current_task = agent.get("current_task_title", "-")

            symbol = status_symbols.get(status, "⚪")

            # Truncate long task titles
            if len(current_task) > 40:
                current_task = current_task[:37] + "..."

            table.add_row(
                f"{symbol} {name}",
                agent_type,
                status,
                current_task,
            )

        return table

    def render_tasks_table(self, tasks: List[Dict[str, Any]]) -> Table:
        """Render tasks table."""
        table = Table(
            title="Recent Tasks",
            show_header=True,
            header_style="bold green",
            border_style="green",
        )

        table.add_column("ID", style="dim", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("Status", style="yellow")
        table.add_column("Priority", style="cyan")
        table.add_column("Assigned To", style="blue")

        # Status symbols
        status_symbols = {
            "backlog": "📋",
            "todo": "📌",
            "assigned": "👤",
            "in_progress": "🔄",
            "review": "👁️",
            "completed": "✅",
            "blocked": "🚫",
        }

        # Priority colors
        priority_colors = {
            1: "red",
            2: "yellow",
            3: "blue",
            4: "green",
        }

        for task in tasks[:10]:  # Show only 10 most recent
            task_id = str(task.get("id", ""))[:8]
            title = task.get("title", "Untitled")
            status = task.get("status", "backlog")
            priority = task.get("priority", 3)
            assigned_to = task.get("assigned_to_name", "-")

            symbol = status_symbols.get(status, "📋")
            priority_color = priority_colors.get(priority, "white")

            # Truncate long titles
            if len(title) > 50:
                title = title[:47] + "..."

            table.add_row(
                task_id,
                f"{symbol} {title}",
                status,
                f"[{priority_color}]P{priority}[/{priority_color}]",
                assigned_to,
            )

        return table

    def render_full_status(
        self,
        project: Dict[str, Any],
        agents: List[Dict[str, Any]],
        tasks: List[Dict[str, Any]],
    ) -> None:
        """Render full status view."""
        # Project status
        self.console.print(self.render_project_status(project))
        self.console.print()

        # Agents
        if agents:
            self.console.print(self.render_agents_table(agents))
            self.console.print()

        # Tasks
        if tasks:
            self.console.print(self.render_tasks_table(tasks))
            self.console.print()

    def render_simple_status(self, status_data: Dict[str, Any]) -> None:
        """Render simple status summary."""
        project_status = status_data.get("project_status", "unknown")
        agents_working = status_data.get("agents_working", 0)
        tasks_in_progress = status_data.get("tasks_in_progress", 0)
        tasks_completed = status_data.get("tasks_completed", 0)

        content = f"[bold cyan]Project:[/bold cyan] {project_status}\n"
        content += f"[bold green]Agents Working:[/bold green] {agents_working}\n"
        content += f"[bold yellow]Tasks In Progress:[/bold yellow] {tasks_in_progress}\n"
        content += f"[bold blue]Tasks Completed:[/bold blue] {tasks_completed}"

        panel = Panel(
            content,
            title="[bold]Status[/bold]",
            border_style="cyan",
            padding=(0, 1),
        )

        self.console.print(panel)

    def render_agent_details(self, agent: Dict[str, Any]) -> None:
        """Render detailed agent information."""
        agent_type = agent.get("agent_type", {})
        name = agent_type.get("name", "Unknown")
        role = agent_type.get("role", "unknown")
        status = agent.get("status", "idle")
        status_message = agent.get("status_message", "")

        content = f"[bold]Agent:[/bold] {name}\n"
        content += f"[bold]Role:[/bold] {role}\n"
        content += f"[bold]Status:[/bold] {status}\n"

        if status_message:
            content += f"[bold]Message:[/bold] {status_message}\n"

        # Statistics
        tasks_completed = agent.get("tasks_completed", 0)
        errors = agent.get("errors_encountered", 0)

        content += f"\n[bold]Statistics:[/bold]\n"
        content += f"  Tasks Completed: {tasks_completed}\n"
        content += f"  Errors: {errors}\n"

        # Current task
        current_task = agent.get("current_task")
        if current_task:
            content += f"\n[bold]Current Task:[/bold]\n"
            content += f"  {current_task.get('title', 'Untitled')}\n"

        panel = Panel(
            content,
            title=f"[bold cyan]{name}[/bold cyan]",
            border_style="cyan",
            padding=(0, 1),
        )

        self.console.print(panel)

    def show_welcome(self, project_name: Optional[str] = None) -> None:
        """Show welcome message."""
        if project_name:
            text = Text.from_markup(
                f"[bold cyan]Welcome to DEVO[/bold cyan]\n"
                f"Project: [bold]{project_name}[/bold]"
            )
        else:
            text = Text.from_markup("[bold cyan]Welcome to DEVO[/bold cyan]")

        panel = Panel(
            text,
            border_style="cyan",
            padding=(1, 2),
        )

        self.console.print(panel)
        self.console.print()

    def show_error(self, message: str) -> None:
        """Show error message."""
        panel = Panel(
            f"[bold red]{message}[/bold red]",
            title="[bold red]Error[/bold red]",
            border_style="red",
            padding=(0, 1),
        )

        self.console.print(panel)

    def show_success(self, message: str) -> None:
        """Show success message."""
        panel = Panel(
            f"[bold green]{message}[/bold green]",
            title="[bold green]Success[/bold green]",
            border_style="green",
            padding=(0, 1),
        )

        self.console.print(panel)

    def show_info(self, message: str) -> None:
        """Show info message."""
        panel = Panel(
            f"[bold blue]{message}[/bold blue]",
            title="[bold blue]Info[/bold blue]",
            border_style="blue",
            padding=(0, 1),
        )

        self.console.print(panel)
