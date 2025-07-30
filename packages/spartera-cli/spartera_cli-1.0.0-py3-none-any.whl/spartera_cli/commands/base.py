"""
Base command class for CLI commands.
"""
import typer
from rich.console import Console
from typing import Optional
from ..client import SparteraClient
from ..utils.formatting import format_output, OutputFormat
from ..utils.config import get_config

console = Console()

class BaseCommand:
    """Base class for CLI commands."""
    
    def __init__(self):
        self.client = SparteraClient()
        self.config = get_config()
    
    def get_company_id(self, company_id: Optional[str] = None) -> str:
        """Get company ID from parameter or config."""
        if company_id:
            return company_id
        
        config_company_id = self.config.get("company_id")
        if not config_company_id:
            console.print("[red]No company ID found. Run 'spartera auth login' first.[/red]")
            raise typer.Exit(1)
        
        return config_company_id
    
    def handle_response(self, response, format_type: OutputFormat = OutputFormat.JSON, success_message: str = None):
        """Handle API response and format output."""
        if response.status_code >= 400:
            self._handle_error(response)
            return
        
        try:
            data = response.json()
            if data.get("message") == "success":
                result_data = data.get("data", data)
                
                if success_message:
                    console.print(f"[green]{success_message}[/green]")
                
                if result_data:
                    format_output(result_data, format_type)
            else:
                console.print(f"[red]Error: {data.get('message', 'Unknown error')}[/red]")
        except Exception as e:
            console.print(f"[red]Error parsing response: {e}[/red]")
    
    def _handle_error(self, response):
        """Handle error responses."""
        try:
            error_data = response.json()
            message = error_data.get("message", "Unknown error")
            details = error_data.get("details", "")
            
            if details:
                console.print(f"[red]Error ({response.status_code}): {message}[/red]")
                console.print(f"[red]Details: {details}[/red]")
            else:
                console.print(f"[red]Error ({response.status_code}): {message}[/red]")
        except:
            console.print(f"[red]HTTP Error {response.status_code}[/red]")
