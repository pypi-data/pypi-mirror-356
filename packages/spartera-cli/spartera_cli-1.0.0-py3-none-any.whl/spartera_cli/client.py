"""
Spartera API Client
"""
import httpx
from typing import Dict, Any, Optional
from rich.console import Console

from .utils.auth import get_api_key
from .utils.config import get_config

console = Console()

class SparteraClient:
    """HTTP client for Spartera API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or get_api_key()
        self.base_url = base_url or "https://api.spartera.com"
        self.client = httpx.Client(base_url=self.base_url, timeout=30.0)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "spartera/1.0.0"
        }
        
        if self.api_key:
            headers["x-api-key"] = self.api_key
            
        return headers
    
    def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """Make authenticated API request."""
        headers = self._get_headers()
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
        kwargs["headers"] = headers
        
        try:
            response = self.client.request(method, path, **kwargs)
            return response
        except httpx.TimeoutException:
            console.print("[red]Request timed out. Please try again.[/red]")
            raise typer.Exit(1)
        except httpx.ConnectError:
            console.print("[red]Connection error. Please check your internet connection.[/red]")
            raise typer.Exit(1)
    
    def get(self, path: str, **kwargs) -> httpx.Response:
        """Make GET request."""
        return self.request("GET", path, **kwargs)
    
    def post(self, path: str, **kwargs) -> httpx.Response:
        """Make POST request."""
        return self.request("POST", path, **kwargs)
    
    def patch(self, path: str, **kwargs) -> httpx.Response:
        """Make PATCH request."""
        return self.request("PATCH", path, **kwargs)
    
    def delete(self, path: str, **kwargs) -> httpx.Response:
        """Make DELETE request."""
        return self.request("DELETE", path, **kwargs)
