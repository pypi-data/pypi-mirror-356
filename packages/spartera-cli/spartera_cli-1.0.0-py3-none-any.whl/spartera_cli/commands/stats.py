"""
Analytics and statistics commands.
"""
import typer
from rich.console import Console
from typing import Optional
from .base import BaseCommand
from ..utils.formatting import OutputFormat

app = typer.Typer()
console = Console()

@app.command()
def company(
    company_id: Optional[str] = typer.Option(None, help="Company ID"),
    format: OutputFormat = typer.Option(OutputFormat.JSON, "--format", "-f", help="Output format")
):
    """Get company analytics dashboard."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    response = cmd.client.get(f"/companies/{company_id}/analytics/dashboard")
    cmd.handle_response(response, format)

@app.command()
def assets(
    company_id: Optional[str] = typer.Option(None, help="Company ID"),
    format: OutputFormat = typer.Option(OutputFormat.JSON, "--format", "-f", help="Output format")
):
    """Get asset statistics."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    response = cmd.client.get(f"/companies/{company_id}/assets/statistics")
    cmd.handle_response(response, format)

@app.command()
def sales(
    company_id: Optional[str] = typer.Option(None, help="Company ID"),
    format: OutputFormat = typer.Option(OutputFormat.JSON, "--format", "-f", help="Output format"),
    start_date: Optional[str] = typer.Option(None, help="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = typer.Option(None, help="End date (YYYY-MM-DD)")
):
    """Get sales analytics."""
    cmd = BaseCommand()
    company_id = cmd.get_company_id(company_id)
    
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    
    response = cmd.client.get(f"/companies/{company_id}/analytics/sales", params=params)
    cmd.handle_response(response, format)
