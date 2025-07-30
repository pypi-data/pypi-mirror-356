"""
Asset management commands.
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
    format: OutputFormat = typer.Option(OutputFormat.TABLE, "--format", "-f", help="Output format"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Limit number of results"),
    page: Optional[int] = typer.Option(None, "--page", "-p", help="Page number"),
    active: Optional[str] = typer.Option("1", help="Filter by active status")
):
    """List all assets."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    params = {"active": active}
    if limit:
        params["limit"] = limit
    if page:
        params["page"] = page
    
    response = cmd.client.get(f"/companies/{company_id}/assets", params=params)
    cmd.handle_response(response, format)

@app.command()
def get(
    asset_id: str,
    company_id: Optional[str] = typer.Option(None, help="Company ID"),
    format: OutputFormat = typer.Option(OutputFormat.JSON, "--format", "-f", help="Output format")
):
    """Get a specific asset."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    response = cmd.client.get(f"/companies/{company_id}/assets/{asset_id}")
    cmd.handle_response(response, format)

@app.command()
def create(
    company_id: Optional[str] = typer.Option(None, help="Company ID"),
    name: Optional[str] = typer.Option(None, help="Asset name"),
    description: Optional[str] = typer.Option(None, help="Asset description"),
    asset_type: Optional[str] = typer.Option(None, help="Asset type (calculation, visualization, etc.)"),
    config_file: Optional[str] = typer.Option(None, "--config", help="Path to config file")
):
    """Create a new asset."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    if config_file:
        console.print("📁 [yellow]Config file creation coming soon![/yellow]")
        return
    
    # Interactive creation
    if not name:
        name = typer.prompt("Asset name")
    if not description:
        description = typer.prompt("Asset description")
    if not asset_type:
        asset_type = typer.prompt("Asset type", default="calculation")
    
    payload = {
        "name": name,
        "description": description,
        "asset_type": asset_type,
        "source": "cli"
    }
    
    response = cmd.client.post(f"/companies/{company_id}/assets", json=payload)
    cmd.handle_response(response, success_message="Asset created successfully")

@app.command()
def delete(
    asset_id: str,
    company_id: Optional[str] = typer.Option(None, help="Company ID"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation")
):
    """Delete an asset."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    if not confirm:
        if not typer.confirm(f"Are you sure you want to delete asset {asset_id}?"):
            console.print("Cancelled.")
            raise typer.Exit()
    
    response = cmd.client.delete(f"/companies/{company_id}/assets/{asset_id}")
    cmd.handle_response(response, success_message="Asset deleted successfully")
