"""
User management commands.
"""
import typer
from rich.console import Console
from typing import Optional
from .base import BaseCommand
from ..utils.formatting import OutputFormat

app = typer.Typer()
console = Console()

@app.command()
def list(
    company_id: Optional[str] = typer.Option(None, help="Company ID"),
    format: OutputFormat = typer.Option(OutputFormat.TABLE, "--format", "-f", help="Output format")
):
    """List all users in company."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    response = cmd.client.get(f"/companies/{company_id}/users")
    cmd.handle_response(response, format)

@app.command()
def get(
    user_id: str,
    company_id: Optional[str] = typer.Option(None, help="Company ID"),
    format: OutputFormat = typer.Option(OutputFormat.JSON, "--format", "-f", help="Output format")
):
    """Get a specific user."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    response = cmd.client.get(f"/companies/{company_id}/users/{user_id}")
    cmd.handle_response(response, format)

@app.command()
def whoami(
    format: OutputFormat = typer.Option(OutputFormat.JSON, "--format", "-f", help="Output format")
):
    """Show current user information."""
    cmd = BaseCommand()
    
    response = cmd.client.get("/me")
    cmd.handle_response(response, format)
