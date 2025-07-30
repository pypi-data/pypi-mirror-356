"""
Authentication commands.
"""
import typer
from rich.console import Console
from rich.prompt import Prompt
from .base import BaseCommand
from ..utils.auth import save_api_key, get_api_key, clear_auth
from ..utils.config import save_config, get_config

app = typer.Typer()
console = Console()

@app.command()
def login():
    """Authenticate with Spartera API."""
    console.print("🔐 [bold]Spartera CLI Authentication[/bold]")
    console.print()
    console.print("To get your API key:")
    console.print("1. Go to [link]https://app.spartera.com[/link]")
    console.print("2. Navigate to Settings → API Keys")
    console.print("3. Click 'Create API Key'")
    console.print("4. Copy the generated key")
    console.print()
    
    api_key = Prompt.ask("Enter your API key", password=True)
    
    if not api_key:
        console.print("[red]No API key provided[/red]")
        raise typer.Exit(1)
    
    # Save API key
    save_api_key(api_key)
    
    # Test the API key
    console.print("🧪 Testing API key...")
    
    try:
        from ..client import SparteraClient
        client = SparteraClient(api_key=api_key)
        response = client.get("/me")
        
        if response.status_code == 200:
            data = response.json()
            user_info = data.get("profile", {})
            company_id = data.get("company_id")
            user_id = user_info.get("id")
            
            console.print("✅ [green]Authentication successful![/green]")
            console.print(f"   User: {user_info.get('email_address', 'Unknown')}")
            console.print(f"   Company ID: {company_id}")
            
            # Save user context
            config = get_config()
            config.update({
                "company_id": company_id,
                "user_id": user_id,
                "email": user_info.get("email_address")
            })
            save_config(config)
            
        else:
            console.print(f"[red]Authentication failed: {response.status_code}[/red]")
            try:
                error_data = response.json()
                console.print(f"[red]{error_data.get('message', 'Unknown error')}[/red]")
            except:
                pass
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]Error testing API key: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def status():
    """Show authentication status."""
    cmd = BaseCommand()
    
    api_key = get_api_key()
    if not api_key:
        console.print("[red]Not authenticated[/red]")
        console.print("Run [bold]spartera auth login[/bold] to authenticate")
        raise typer.Exit(1)
    
    try:
        response = cmd.client.get("/me")
        cmd.handle_response(response)
    except Exception as e:
        console.print(f"[red]Authentication error: {e}[/red]")
        console.print("Run [bold]spartera auth login[/bold] to re-authenticate")
        raise typer.Exit(1)

@app.command()
def logout():
    """Clear stored authentication."""
    clear_auth()
    console.print("✅ [green]Logged out successfully[/green]")
