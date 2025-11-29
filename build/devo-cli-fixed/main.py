"""
Main CLI application for DEVO.

Interactive command-line interface for the DEVO multi-agent development system.
"""
import asyncio
import sys
from typing import Optional
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm

from .config import config
from .client import APIClient, APIError, WebSocketClient
from .ui import ChatPanel, StatusPanel
from .commands import chat as chat_commands

# Create Typer app
app = typer.Typer(
    name="devo",
    help="DEVO - Multi-Agent AI Development System",
    add_completion=False,
)

# Create console
console = Console()


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    """
    Default behavior when no command is provided.

    This mimics Claude Code behavior:
    1. Check if user is authenticated
    2. If not, prompt for login
    3. Get or create default project
    4. Start interactive chat session
    """
    # If a subcommand was invoked, don't run default behavior
    if ctx.invoked_subcommand is not None:
        return

    # Run interactive session
    asyncio.run(_interactive_session())


async def _interactive_session() -> None:
    """Interactive session - login and chat."""
    from .commands.chat import ChatSession

    status_panel = StatusPanel(console)

    # Check authentication
    api_key = config.get_api_key()

    if not api_key:
        # Not logged in - prompt for login
        console.print("\n[bold cyan]Welcome to DEVO[/bold cyan]")
        console.print("[dim]Multi-Agent AI Development System[/dim]\n")
        console.print("[yellow]Please login to continue[/yellow]\n")

        email = Prompt.ask("Email")
        password = Prompt.ask("Password", password=True)

        try:
            async with APIClient() as client:
                with console.status("[bold blue]Logging in..."):
                    response = await client.login(email, password)

                # Extract token from nested structure
                tokens = response.get("tokens", {})
                api_key = tokens.get("access")

                if api_key:
                    # Save credentials
                    config.set_api_key(api_key)

                    # Extract user info from login response
                    user = response.get("user", {})
                    username = user.get("username", "")

                    config.set("email", email)
                    config.set("username", username)

                    console.print(f"\n[green]✓[/green] Logged in as [cyan]{username}[/cyan]\n")
                else:
                    status_panel.show_error("Login failed: No token received")
                    sys.exit(1)

        except APIError as e:
            status_panel.show_error(f"Login failed: {e.message}")
            sys.exit(1)
    else:
        # Already logged in
        username = config.get("username", "User")
        console.print(f"\n[bold cyan]Welcome back, {username}![/bold cyan]\n")

    # Get or create default project
    try:
        async with APIClient() as client:
            # Check if we have a last project
            project_id = config.get("last_project_id")

            if project_id:
                # Try to get existing project
                try:
                    project = await client.get_project(project_id)
                except APIError:
                    # Project doesn't exist, create default
                    project_id = None

            if not project_id:
                # Create or get default project
                with console.status("[bold blue]Setting up your workspace..."):
                    projects = await client.list_projects()

                    # Look for a default project
                    default_project = None
                    for p in projects:
                        if p.get("name") == "default" or p.get("name") == "Default":
                            default_project = p
                            break

                    if default_project:
                        project_id = default_project.get("id")
                        config.set("last_project_id", project_id)
                    else:
                        # Create default project
                        project = await client.create_project(
                            name="default",
                            description="Default DEVO workspace",
                        )
                        project_id = project.get("id")
                        config.set("last_project_id", project_id)

            console.print("[dim]Type /help for available commands, /exit to quit[/dim]\n")

            # Start chat session
            session = ChatSession(project_id=project_id, console=console)
            await session.start()

    except APIError as e:
        status_panel.show_error(f"Failed to setup workspace: {e.message}")
        sys.exit(1)
    except Exception as e:
        status_panel.show_error(f"Unexpected error: {str(e)}")
        sys.exit(1)


@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Project description"),
):
    """Initialize a new DEVO project."""
    asyncio.run(_init_project(name, description))


async def _init_project(name: str, description: Optional[str]) -> None:
    """Initialize project implementation."""
    status_panel = StatusPanel(console)

    try:
        async with APIClient() as client:
            # Check if API is accessible
            with console.status("[bold blue]Connecting to DEVO backend..."):
                healthy = await client.health_check()

            if not healthy:
                status_panel.show_error("Could not connect to DEVO backend. Is it running?")
                sys.exit(1)

            # Create project
            with console.status(f"[bold blue]Creating project '{name}'..."):
                project = await client.create_project(
                    name=name,
                    description=description,
                )

            project_id = project.get("id")

            # Save as default project
            config.set("last_project_id", project_id)

            status_panel.show_success(
                f"Project '{name}' created successfully!\n"
                f"Project ID: {project_id}\n\n"
                f"Start chatting with: devo chat"
            )

    except APIError as e:
        status_panel.show_error(f"Failed to create project: {e.message}")
        sys.exit(1)
    except Exception as e:
        status_panel.show_error(f"Unexpected error: {str(e)}")
        sys.exit(1)


@app.command()
def chat(
    project_id: Optional[str] = typer.Option(None, "--project", "-p", help="Project ID"),
    resume: bool = typer.Option(False, "--resume", "-r", help="Resume last session"),
):
    """Start interactive chat session."""
    asyncio.run(_chat_session(project_id, resume))


async def _chat_session(project_id: Optional[str], resume: bool) -> None:
    """Chat session implementation."""
    from .commands.chat import ChatSession

    # Get project ID
    if not project_id:
        project_id = config.get("last_project_id")

    if not project_id:
        status_panel = StatusPanel(console)
        status_panel.show_error(
            "No project specified. Create one with: devo init <project-name>"
        )
        sys.exit(1)

    # Start chat session
    session = ChatSession(project_id=project_id, console=console)
    await session.start()


@app.command()
def status(
    project_id: Optional[str] = typer.Option(None, "--project", "-p", help="Project ID"),
):
    """Show project status."""
    asyncio.run(_show_status(project_id))


async def _show_status(project_id: Optional[str]) -> None:
    """Show status implementation."""
    status_panel = StatusPanel(console)

    # Get project ID
    if not project_id:
        project_id = config.get("last_project_id")

    if not project_id:
        status_panel.show_error("No project specified")
        sys.exit(1)

    try:
        async with APIClient() as client:
            # Get project
            with console.status("[bold blue]Loading project status..."):
                project = await client.get_project(project_id)
                agents = await client.get_project_agents(project_id)
                tasks = await client.list_tasks(project_id)

            # Render status
            status_panel.render_full_status(project, agents, tasks)

    except APIError as e:
        status_panel.show_error(f"Failed to get status: {e.message}")
        sys.exit(1)


@app.command()
def agents(
    project_id: Optional[str] = typer.Option(None, "--project", "-p", help="Project ID"),
):
    """List agents in project."""
    asyncio.run(_list_agents(project_id))


async def _list_agents(project_id: Optional[str]) -> None:
    """List agents implementation."""
    status_panel = StatusPanel(console)

    # Get project ID
    if not project_id:
        project_id = config.get("last_project_id")

    if not project_id:
        status_panel.show_error("No project specified")
        sys.exit(1)

    try:
        async with APIClient() as client:
            # Get agents
            with console.status("[bold blue]Loading agents..."):
                agents = await client.get_project_agents(project_id)

            if not agents:
                status_panel.show_info("No agents in this project yet")
                return

            # Render agents table
            table = status_panel.render_agents_table(agents)
            console.print(table)

    except APIError as e:
        status_panel.show_error(f"Failed to list agents: {e.message}")
        sys.exit(1)


@app.command()
def projects():
    """List all projects."""
    asyncio.run(_list_projects())


async def _list_projects() -> None:
    """List projects implementation."""
    from rich.table import Table

    status_panel = StatusPanel(console)

    try:
        async with APIClient() as client:
            # Get projects
            with console.status("[bold blue]Loading projects..."):
                projects = await client.list_projects()

            if not projects:
                status_panel.show_info("No projects yet. Create one with: devo init <name>")
                return

            # Create table
            table = Table(
                title="Projects",
                show_header=True,
                header_style="bold cyan",
                border_style="cyan",
            )

            table.add_column("ID", style="dim", no_wrap=True)
            table.add_column("Name", style="cyan")
            table.add_column("Status", style="yellow")
            table.add_column("Description", style="white")

            for project in projects:
                project_id = str(project.get("id", ""))[:8]
                name = project.get("name", "Unknown")
                status = project.get("status", "unknown")
                description = project.get("description", "")

                # Truncate long descriptions
                if len(description) > 60:
                    description = description[:57] + "..."

                table.add_row(project_id, name, status, description)

            console.print(table)

    except APIError as e:
        status_panel.show_error(f"Failed to list projects: {e.message}")
        sys.exit(1)


@app.command()
def configure(
    key: Optional[str] = typer.Argument(None, help="Configuration key"),
    value: Optional[str] = typer.Argument(None, help="Configuration value"),
    list_all: bool = typer.Option(False, "--list", "-l", help="List all configuration"),
):
    """Configure DEVO settings."""
    status_panel = StatusPanel(console)

    if list_all:
        # List all configuration
        all_config = config.list_all()

        from rich.table import Table

        table = Table(
            title="Configuration",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
        )

        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")

        for k, v in all_config.items():
            # Hide sensitive values
            if k in ["api_key"]:
                if v:
                    v = "***" + str(v)[-4:]
                else:
                    v = "Not set"

            table.add_row(k, str(v))

        console.print(table)
        return

    if key and value:
        # Set configuration
        try:
            config.set(key, value)
            status_panel.show_success(f"Set {key} = {value}")
        except KeyError as e:
            status_panel.show_error(str(e))
            sys.exit(1)
    elif key:
        # Get configuration
        value = config.get(key)
        console.print(f"{key} = {value}")
    else:
        status_panel.show_error("Usage: devo configure <key> <value> or devo configure --list")
        sys.exit(1)


@app.command()
def login():
    """Login to DEVO."""
    asyncio.run(_login())


async def _login() -> None:
    """Login implementation."""
    status_panel = StatusPanel(console)

    console.print("[bold cyan]DEVO Login[/bold cyan]\n")

    email = Prompt.ask("Email")
    password = Prompt.ask("Password", password=True)

    # Clear any existing API key to avoid sending invalid token during login
    config.set_api_key("")

    try:
        async with APIClient() as client:
            with console.status("[bold blue]Logging in..."):
                response = await client.login(email, password)

            # Extract token from nested structure
            tokens = response.get("tokens", {})
            api_key = tokens.get("access")

            if api_key:
                # Save API key
                config.set_api_key(api_key)

                # Extract user info from login response
                user = response.get("user", {})
                username = user.get("username", "")

                config.set("email", email)
                config.set("username", username)

                status_panel.show_success(f"Logged in as {username}")
            else:
                status_panel.show_error("Login failed: No token received")
                sys.exit(1)

    except APIError as e:
        status_panel.show_error(f"Login failed: {e.message}")
        sys.exit(1)


@app.command()
def logout():
    """Logout from DEVO."""
    config.set_api_key("")
    config.set("email", "")
    config.set("username", "")

    status_panel = StatusPanel(console)
    status_panel.show_success("Logged out successfully")


@app.command()
def version():
    """Show DEVO version."""
    console.print("[bold cyan]DEVO CLI v0.1.0[/bold cyan]")
    console.print("Multi-Agent AI Development System")


def main():
    """Entry point for CLI."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
