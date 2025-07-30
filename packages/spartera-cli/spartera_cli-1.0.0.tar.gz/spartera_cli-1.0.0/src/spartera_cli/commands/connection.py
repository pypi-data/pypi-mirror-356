"""
Connection management commands.
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
    """List all connections."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    response = cmd.client.get(f"/companies/{company_id}/connections")
    cmd.handle_response(response, format)

@app.command()
def get(
    connection_id: str,
    company_id: Optional[str] = typer.Option(None, help="Company ID"),
    format: OutputFormat = typer.Option(OutputFormat.JSON, "--format", "-f", help="Output format")
):
    """Get a specific connection."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    response = cmd.client.get(f"/companies/{company_id}/connections/{connection_id}")
    cmd.handle_response(response, format)

@app.command()
def create(
    company_id: Optional[str] = typer.Option(None, help="Company ID"),
    name: Optional[str] = typer.Option(None, help="Connection name"),
    provider: Optional[str] = typer.Option(None, help="Provider (bigquery, redshift, etc.)"),
    credentials_file: Optional[str] = typer.Option(None, help="Path to credentials file")
):
    """Create a new connection."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    console.print("🔗 [bold]Create New Connection[/bold]")
    console.print()
    
    if not name:
        name = typer.prompt("Connection name")
    
    if not provider:
        providers = ["bigquery", "redshift", "snowflake", "azure_sql", "teradata"]
        console.print("Available providers:")
        for i, p in enumerate(providers, 1):
            console.print(f"  {i}. {p}")
        
        choice = typer.prompt("Select provider (1-5)", type=int)
        if 1 <= choice <= len(providers):
            provider = providers[choice - 1]
        else:
            console.print("[red]Invalid choice[/red]")
            raise typer.Exit(1)
    
    payload = {
        "name": name,
        "provider": provider,
    }
    
    if credentials_file:
        try:
            import json
            with open(credentials_file, 'r') as f:
                if credentials_file.endswith('.json'):
                    credentials = json.load(f)
                    payload["credentials"] = json.dumps(credentials)
                else:
                    payload["credentials"] = f.read()
        except Exception as e:
            console.print(f"[red]Error reading credentials file: {e}[/red]")
            raise typer.Exit(1)
    else:
        console.print("📝 [yellow]Interactive credential input coming soon![/yellow]")
        console.print("For now, please provide credentials file with --credentials-file")
        return
    
    response = cmd.client.post(f"/companies/{company_id}/connections", json=payload)
    cmd.handle_response(response, success_message="Connection created successfully")

@app.command()
def test(
    connection_id: str,
    company_id: Optional[str] = typer.Option(None, help="Company ID")
):
    """Test a connection."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    console.print(f"🧪 Testing connection {connection_id}...")
    response = cmd.client.get(f"/companies/{company_id}/connections/{connection_id}/test")
    cmd.handle_response(response, success_message="Connection test completed")

@app.command()
def delete(
    connection_id: str,
    company_id: Optional[str] = typer.Option(None, help="Company ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation")
):
    """Delete a connection."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    if not confirm:
        if not typer.confirm(f"Are you sure you want to delete connection {connection_id}?"):
            console.print("Cancelled.")
            raise typer.Exit()
    
    response = cmd.client.delete(f"/companies/{company_id}/connections/{connection_id}")
    cmd.handle_response(response, success_message="Connection deleted successfully")
