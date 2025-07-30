#!/usr/bin/env python3
"""
Spartera CLI - Main Entry Point
"""
import typer
from rich.console import Console

from .commands import auth, asset, connection, process, user, stats
from .__init__ import __version__

app = typer.Typer(
    name="spartera",
    help="Official CLI for Spartera API platform",
    rich_markup_mode="rich"
)

console = Console()

# Add command groups
app.add_typer(auth.app, name="auth", help="Authentication commands")
app.add_typer(asset.app, name="asset", help="Asset management")  
app.add_typer(connection.app, name="connection", help="Connection management")
app.add_typer(process.app, name="process", help="Process/analyze assets")
app.add_typer(user.app, name="user", help="User management")
app.add_typer(stats.app, name="stats", help="Analytics and statistics")

@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Show version"),
    verbose: bool = typer.Option(False, "--verbose", help="Enable verbose output")
):
    """Official CLI for Spartera API platform"""
    if version:
        console.print(f"spartera version {__version__}")
        raise typer.Exit()

def cli():
    """Entry point for CLI."""
    app()

if __name__ == "__main__":
    cli()
