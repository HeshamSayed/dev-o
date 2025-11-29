#!/usr/bin/env python3
"""
Devo CLI entry point for direct execution
"""
import sys
import os

# Add CLI directory to path
cli_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, cli_dir)

# Now import and run the main app
import typer
from rich.console import Console
from config import config
from commands.chat import ChatSession
from commands.login import login_command
from commands.project import list_projects, create_project, switch_project

app = typer.Typer(
    name="devo",
    help="Devo CLI - AI-powered development assistant",
    add_completion=False
)

app.command(name="login")(login_command)
app.command(name="projects")(list_projects)
app.command(name="create-project")(create_project)
app.command(name="switch")(switch_project)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Start interactive chat session if no command specified."""
    if ctx.invoked_subcommand is None:
        # Start interactive chat
        import asyncio
        console = Console()

        # Get current project
        current_project = config.current_project
        if not current_project:
            console.print("[red]No project selected. Please run 'devo projects' and 'devo switch <project-id>'[/red]")
            raise typer.Exit(1)

        session = ChatSession(project_id=current_project, console=console)
        asyncio.run(session.start())

if __name__ == "__main__":
    app()
