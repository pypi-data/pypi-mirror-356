#!/usr/bin/env python3
"""
Spartera CLI Complete Generator
==============================
Generates the complete Spartera CLI application from your swagger.yaml.

Usage:
    python spartera_cli_generator.py [--swagger path/to/swagger.yaml] [--version 1.0.0]
"""

import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict
from dataclasses import dataclass


@dataclass
class CLIConfig:
    api_name: str = "spartera-api"
    api_version: str = "1.0.0"
    cli_name: str = "spartera"
    package_name: str = "spartera_cli"
    description: str = "Official CLI for Spartera API platform"
    author: str = "Tony D"
    author_email: str = "tony@spartera.com"
    github_url: str = "https://github.com/spartera-com/spartera-cli"
    api_base_url: str = "https://api.spartera.com"


class SparteraCLIGenerator:
    def __init__(self, swagger_path: str, version: str = "1.0.0"):
        self.swagger_path = swagger_path
        self.config = CLIConfig(api_version=version)
        self.swagger_spec = self._load_swagger()

    def _load_swagger(self) -> Dict:
        """Load swagger specification."""
        try:
            with open(self.swagger_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading swagger file: {e}")
            sys.exit(1)

    def generate(self, output_dir: str = "./spartera-cli"):
        """Generate complete CLI application."""
        output_path = Path(output_dir)

        print(f"🚀 Generating Spartera CLI v{self.config.api_version}")
        print(f"📁 Output directory: {output_path}")

        # Create directory structure
        self._create_directories(output_path)

        # Generate all files
        self._generate_project_files(output_path)
        self._generate_source_files(output_path)
        self._generate_scripts(output_path)
        self._generate_tests(output_path)
        self._generate_docs(output_path)

        print(f"✅ CLI generated successfully!")
        print(f"🔧 Next steps:")
        print(f"   cd {output_path}")
        print(f"   pip install -e .")
        print(f"   spartera --help")

    def _create_directories(self, output_path: Path):
        """Create directory structure."""
        directories = [
            output_path,
            output_path / "src" / self.config.package_name,
            output_path / "src" / self.config.package_name / "commands",
            output_path / "src" / self.config.package_name / "utils",
            output_path / "tests",
            output_path / "scripts",
            output_path / "docs",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _generate_project_files(self, output_path: Path):
        """Generate project configuration files."""

        # pyproject.toml
        pyproject_content = f'''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{self.config.package_name}"
version = "{self.config.api_version}"
description = "{self.config.description}"
readme = "README.md"
license = {{file = "LICENSE"}}
authors = [
    {{name = "{self.config.author}", email = "{self.config.author_email}"}},
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "typer[all]>=0.9.0",
    "rich>=13.0.0",
    "httpx>=0.24.0",
    "keyring>=24.0.0",
    "pydantic>=2.0.0",
    "pyyaml>=6.0.0",
]
requires-python = ">=3.8"

[project.urls]
Documentation = "{self.config.github_url}"
Repository = "{self.config.github_url}"
"Bug Tracker" = "{self.config.github_url}/issues"

[project.scripts]
{self.config.cli_name} = "{self.config.package_name}.main:cli"

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src/{self.config.package_name}"]

[tool.black]
line-length = 88
target-version = ["py38"]

[tool.isort]
profile = "black"
line_length = 88
'''
        (output_path / "pyproject.toml").write_text(pyproject_content)

        # README.md
        readme_content = f"""# {self.config.cli_name.upper()} CLI

{self.config.description}

## 🚀 Installation

```bash
pip install {self.config.package_name}
```

## 🔐 Authentication

```bash
{self.config.cli_name} auth login
```

Get your API key from [app.spartera.com](https://app.spartera.com) → Settings → API Keys

## 📖 Quick Start

```bash
# List assets
{self.config.cli_name} asset list

# Get asset details
{self.config.cli_name} asset get <asset-id>

# Process an asset
{self.config.cli_name} process <asset-id>

# Process marketplace asset
{self.config.cli_name} process company-handle/asset-slug

# Save results to file
{self.config.cli_name} process <asset-id> --output results.json

# Get SVG visualization
{self.config.cli_name} process <asset-id> --svg --output chart.svg
```

## 📋 Commands

### Authentication
- `{self.config.cli_name} auth login` - Authenticate with API key
- `{self.config.cli_name} auth status` - Show current user info
- `{self.config.cli_name} auth logout` - Clear credentials

### Assets
- `{self.config.cli_name} asset list` - List assets
- `{self.config.cli_name} asset get <id>` - Get asset details
- `{self.config.cli_name} asset create` - Create asset
- `{self.config.cli_name} asset delete <id>` - Delete asset

### Connections
- `{self.config.cli_name} connection list` - List connections
- `{self.config.cli_name} connection create` - Create connection
- `{self.config.cli_name} connection test <id>` - Test connection

### Processing
- `{self.config.cli_name} process <asset-ref>` - Process/analyze asset

### Output Formats
- `--format json|table|csv` - Output format
- `--output FILE` - Save to file

## 🛠️ Development

```bash
git clone {self.config.github_url}
cd spartera-cli
pip install -e ".[dev]"
```

## 📞 Support

- **Issues**: [{self.config.github_url}/issues]({self.config.github_url}/issues)
- **Email**: {self.config.author_email}
"""
        (output_path / "README.md").write_text(readme_content)

        # LICENSE
        license_content = """MIT License

Copyright (c) 2024 Spartera Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        (output_path / "LICENSE").write_text(license_content)

        # .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# CLI specific
.spartera/
*.log
"""
        (output_path / ".gitignore").write_text(gitignore_content)

    def _generate_source_files(self, output_path: Path):
        """Generate main source files."""
        src_path = output_path / "src" / self.config.package_name

        # __init__.py
        init_content = f'''"""Spartera CLI package."""
__version__ = "{self.config.api_version}"
'''
        (src_path / "__init__.py").write_text(init_content)

        # main.py - CLI entry point
        main_content = f'''#!/usr/bin/env python3
"""
Spartera CLI - Main Entry Point
"""
import typer
from rich.console import Console

from .commands import auth, asset, connection, process, user, stats
from .__init__ import __version__

app = typer.Typer(
    name="{self.config.cli_name}",
    help="{self.config.description}",
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
    """{self.config.description}"""
    if version:
        console.print(f"{self.config.cli_name} version {{__version__}}")
        raise typer.Exit()

def cli():
    """Entry point for CLI."""
    app()

if __name__ == "__main__":
    cli()
'''
        (src_path / "main.py").write_text(main_content)

        # client.py - API client
        client_content = f'''"""
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
        self.base_url = base_url or "{self.config.api_base_url}"
        self.client = httpx.Client(base_url=self.base_url, timeout=30.0)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {{
            "Content-Type": "application/json",
            "User-Agent": "{self.config.cli_name}/{self.config.api_version}"
        }}
        
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
'''
        (src_path / "client.py").write_text(client_content)

        # Generate command files
        self._generate_commands(src_path / "commands")

        # Generate utility files
        self._generate_utils(src_path / "utils")

    def _generate_commands(self, commands_path: Path):
        """Generate command modules."""

        # __init__.py
        (commands_path / "__init__.py").write_text('"""CLI command modules."""\n')

        # base.py - Base command class
        base_content = '''"""
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
'''
        (commands_path / "base.py").write_text(base_content)

        # Generate specific command files
        command_files = {
            "auth.py": self._get_auth_commands(),
            "asset.py": self._get_asset_commands(),
            "connection.py": self._get_connection_commands(),
            "process.py": self._get_process_commands(),
            "user.py": self._get_user_commands(),
            "stats.py": self._get_stats_commands(),
        }

        for filename, content in command_files.items():
            (commands_path / filename).write_text(content)

    def _generate_utils(self, utils_path: Path):
        """Generate utility modules."""

        # __init__.py
        (utils_path / "__init__.py").write_text('"""CLI utility modules."""\n')

        # config.py
        config_content = '''"""
Configuration management for Spartera CLI.
"""
import json
from pathlib import Path
from typing import Dict, Any

def get_config_dir() -> Path:
    """Get CLI configuration directory."""
    config_dir = Path.home() / ".spartera"
    config_dir.mkdir(exist_ok=True)
    return config_dir

def get_config_file() -> Path:
    """Get configuration file path."""
    return get_config_dir() / "config.json"

def get_config() -> Dict[str, Any]:
    """Load configuration from file."""
    config_file = get_config_file()
    
    if not config_file.exists():
        return {}
    
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_config(config: Dict[str, Any]):
    """Save configuration to file."""
    config_file = get_config_file()
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

def get_setting(key: str, default: Any = None) -> Any:
    """Get a specific setting."""
    config = get_config()
    return config.get(key, default)

def set_setting(key: str, value: Any):
    """Set a specific setting."""
    config = get_config()
    config[key] = value
    save_config(config)
'''
        (utils_path / "config.py").write_text(config_content)

        # auth.py
        auth_utils_content = '''"""
Authentication utilities for Spartera CLI.
"""
import keyring
from typing import Optional

SERVICE_NAME = "spartera-cli"
API_KEY_USERNAME = "api-key"

def save_api_key(api_key: str):
    """Save API key securely."""
    try:
        keyring.set_password(SERVICE_NAME, API_KEY_USERNAME, api_key)
    except Exception:
        # Fallback to config file if keyring fails
        from .config import set_setting
        set_setting("api_key", api_key)

def get_api_key() -> Optional[str]:
    """Get stored API key."""
    try:
        return keyring.get_password(SERVICE_NAME, API_KEY_USERNAME)
    except Exception:
        # Fallback to config file
        from .config import get_setting
        return get_setting("api_key")

def clear_auth():
    """Clear stored authentication."""
    try:
        keyring.delete_password(SERVICE_NAME, API_KEY_USERNAME)
    except Exception:
        pass
    
    # Also clear from config
    from .config import get_config, save_config
    config = get_config()
    config.pop("api_key", None)
    config.pop("company_id", None)
    config.pop("user_id", None)
    config.pop("email", None)
    save_config(config)
'''
        (utils_path / "auth.py").write_text(auth_utils_content)

        # formatting.py
        formatting_content = '''"""
Output formatting utilities for Spartera CLI.
"""
import json
from enum import Enum
from typing import Any, Dict, List
from rich.console import Console
from rich.table import Table
from rich.json import JSON

console = Console()

class OutputFormat(str, Enum):
    """Output format options."""
    JSON = "json"
    TABLE = "table"
    CSV = "csv"

def format_output(data: Any, format_type: OutputFormat = OutputFormat.JSON):
    """Format and display output based on format type."""
    
    if format_type == OutputFormat.JSON:
        # Pretty print JSON
        if isinstance(data, (dict, list)):
            console.print(JSON.from_data(data))
        else:
            console.print(json.dumps(data, indent=2))
    
    elif format_type == OutputFormat.TABLE:
        # Display as table
        if isinstance(data, list) and data:
            _display_table(data)
        elif isinstance(data, dict):
            _display_dict_table(data)
        else:
            console.print(str(data))
    
    elif format_type == OutputFormat.CSV:
        # Display as CSV
        if isinstance(data, list) and data:
            _display_csv(data)
        else:
            console.print("CSV format only supported for list data")

def _display_table(data: List[Dict]):
    """Display list of dictionaries as table."""
    if not data:
        console.print("No data to display")
        return
    
    # Get all unique keys from all records
    all_keys = set()
    for item in data:
        if isinstance(item, dict):
            all_keys.update(item.keys())
    
    # Create table
    table = Table()
    
    # Add columns (limit to most important ones for readability)
    key_priority = ['name', 'id', 'asset_id', 'connection_id', 'user_id', 'email', 'status', 'date_created']
    sorted_keys = []
    
    # Add priority keys first
    for key in key_priority:
        if key in all_keys:
            sorted_keys.append(key)
            all_keys.remove(key)
    
    # Add remaining keys
    sorted_keys.extend(sorted(all_keys))
    
    # Limit to first 6 columns for readability
    display_keys = sorted_keys[:6]
    
    for key in display_keys:
        table.add_column(key.replace("_", " ").title(), overflow="fold")
    
    # Add rows
    for item in data:
        if isinstance(item, dict):
            row = []
            for key in display_keys:
                value = item.get(key, "")
                # Handle None values and convert to string
                if value is None:
                    value = ""
                elif isinstance(value, (dict, list)):
                    value = str(len(value)) if isinstance(value, list) else "..."
                else:
                    value = str(value)
                
                # Truncate long values
                if len(value) > 50:
                    value = value[:47] + "..."
                    
                row.append(value)
            table.add_row(*row)
    
    console.print(table)
    
    if len(sorted_keys) > 6:
        console.print(f"[dim]Showing {len(display_keys)} of {len(sorted_keys)} columns. Use --format json for full data.[/dim]")

def _display_dict_table(data: Dict):
    """Display dictionary as key-value table."""
    table = Table()
    table.add_column("Key", style="bold")
    table.add_column("Value")
    
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            if isinstance(value, list):
                value = f"[{len(value)} items]"
            else:
                value = "[object]"
        display_value = str(value)
        if len(display_value) > 100:
            display_value = display_value[:97] + "..."
        
        table.add_row(key.replace("_", " ").title(), display_value)
    
    console.print(table)

def _display_csv(data: List[Dict]):
    """Display list of dictionaries as CSV."""
    if not data:
        return
    
    # Get all unique keys
    all_keys = set()
    for item in data:
        if isinstance(item, dict):
            all_keys.update(item.keys())
    
    # Print header
    headers = sorted(all_keys)
    console.print(",".join(headers))
    
    # Print rows
    for item in data:
        if isinstance(item, dict):
            row = []
            for key in headers:
                value = item.get(key, "")
                if value is None:
                    value = ""
                elif isinstance(value, (dict, list)):
                    value = json.dumps(value).replace(",", ";")  # Escape commas
                else:
                    value = str(value).replace(",", ";")  # Escape commas
                row.append(f'"{value}"')  # Quote all values
            console.print(",".join(row))
'''
        (utils_path / "formatting.py").write_text(formatting_content)

    def _get_auth_commands(self) -> str:
        """Generate auth commands."""
        return '''"""
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
'''

    def _get_asset_commands(self) -> str:
        """Generate asset commands."""
        return '''"""
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
'''

    def _get_connection_commands(self) -> str:
        """Generate connection commands."""
        return '''"""
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
'''

    def _get_process_commands(self) -> str:
        """Generate process commands."""
        return '''"""
Asset processing/analysis commands.
"""
import typer
from rich.console import Console
from typing import Optional
from pathlib import Path
import json
from .base import BaseCommand
from ..utils.formatting import OutputFormat

app = typer.Typer()
console = Console()

@app.command()
def analyze(
    asset_ref: str = typer.Argument(help="Asset ID or company_handle/asset_slug"),
    company_id: Optional[str] = typer.Option(None, help="Company ID (for asset ID)"),
    format: OutputFormat = typer.Option(OutputFormat.JSON, "--format", "-f", help="Output format"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Save output to file"),
    svg: bool = typer.Option(False, "--svg", help="Request SVG format for visualizations")
):
    """Process/analyze an asset."""
    cmd = BaseCommand()
    
    # Determine if this is asset_id or company_handle/asset_slug
    if "/" in asset_ref:
        # Public marketplace format: company_handle/asset_slug
        company_handle, asset_slug = asset_ref.split("/", 1)
        endpoint = f"/analyze/{company_handle}/assets/{asset_slug}"
        console.print(f"🔄 Processing marketplace asset: {company_handle}/{asset_slug}")
    else:
        # Private asset format: asset_id
        company_id = cmd.get_company_id(company_id)
        
        # Get asset info first to construct the analyze endpoint
        console.print(f"🔍 Getting asset info for {asset_ref}...")
        asset_response = cmd.client.get(f"/companies/{company_id}/assets/{asset_ref}")
        if asset_response.status_code != 200:
            console.print(f"[red]Could not find asset {asset_ref}[/red]")
            raise typer.Exit(1)
        
        asset_data = asset_response.json().get("data", {})
        
        # Get company info for handle
        company_response = cmd.client.get(f"/companies/{company_id}")
        if company_response.status_code != 200:
            console.print(f"[red]Could not get company info[/red]")
            raise typer.Exit(1)
        
        company_data = company_response.json().get("data", {})
        company_handle = company_data.get("company_handle")
        asset_slug = asset_data.get("slug")
        
        if not company_handle or not asset_slug:
            console.print(f"[red]Missing company_handle or asset_slug[/red]")
            console.print("Asset data:", asset_data)
            console.print("Company data:", company_data)
            raise typer.Exit(1)
        
        endpoint = f"/analyze/{company_handle}/assets/{asset_slug}"
        console.print(f"🔄 Processing private asset: {asset_ref}")
    
    # Add query parameters
    params = {}
    if svg:
        params["format"] = "svg"
    
    # Make the analysis request
    response = cmd.client.get(endpoint, params=params)
    
    if response.status_code == 200:
        if output_file:
            # Save to file
            output_path = Path(output_file)
            
            try:
                response_data = response.json()
                
                if svg and "data" in response_data:
                    # Handle SVG content
                    svg_content = response_data["data"]
                    if isinstance(svg_content, str):
                        output_path.write_text(svg_content)
                        console.print(f"✅ [green]SVG saved to {output_path}[/green]")
                    else:
                        # JSON response with SVG data
                        output_path.write_text(json.dumps(response_data, indent=2))
                        console.print(f"✅ [green]Results saved to {output_path}[/green]")
                else:
                    # Handle JSON content
                    output_path.write_text(json.dumps(response_data, indent=2))
                    console.print(f"✅ [green]Results saved to {output_path}[/green]")
                    
            except Exception as e:
                console.print(f"[red]Error saving file: {e}[/red]")
                # Still show the response
                cmd.handle_response(response, format)
        else:
            cmd.handle_response(response, format)
    else:
        cmd.handle_response(response)

# Alias for common usage
@app.command(name="run")
def run_alias(
    asset_ref: str = typer.Argument(help="Asset ID or company_handle/asset_slug"),
    company_id: Optional[str] = typer.Option(None, help="Company ID (for asset ID)"),
    format: OutputFormat = typer.Option(OutputFormat.JSON, "--format", "-f", help="Output format"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Save output to file"),
    svg: bool = typer.Option(False, "--svg", help="Request SVG format for visualizations")
):
    """Alias for analyze command."""
    analyze(asset_ref, company_id, format, output_file, svg)
'''

    def _get_user_commands(self) -> str:
        """Generate user commands."""
        return '''"""
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
'''

    def _get_stats_commands(self) -> str:
        """Generate stats commands."""
        return '''"""
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
'''

    def _generate_scripts(self, output_path: Path):
        """Generate build and test scripts."""
        scripts_path = output_path / "scripts"

        # build.sh
        build_script = f"""#!/bin/bash
set -e

echo "🔨 Building Spartera CLI..."

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
pip install build twine

# Build package
python -m build

# Verify package
twine check dist/*

echo "✅ Build completed successfully!"
echo "📦 Packages created in dist/"
"""
        (scripts_path / "build.sh").write_text(build_script)
        (scripts_path / "build.sh").chmod(0o755)

        # test.sh
        test_script = f"""#!/bin/bash
set -e

echo "🧪 Testing Spartera CLI..."

# Install in development mode
pip install -e .

# Basic functionality tests
{self.config.cli_name} --version
{self.config.cli_name} --help
{self.config.cli_name} auth --help
{self.config.cli_name} asset --help

echo "✅ Basic tests passed!"

# If API key is available, test API connectivity
if [ -n "$SPARTERA_API_KEY" ]; then
    echo "🔗 Testing API connectivity..."
    echo "$SPARTERA_API_KEY" | {self.config.cli_name} auth login --stdin || true
    {self.config.cli_name} auth status || true
else
    echo "⚠️  SPARTERA_API_KEY not set - skipping API tests"
fi
"""
        (scripts_path / "test.sh").write_text(test_script)
        (scripts_path / "test.sh").chmod(0o755)

    def _generate_tests(self, output_path: Path):
        """Generate test files."""
        tests_path = output_path / "tests"

        # conftest.py
        conftest_content = '''"""Test configuration for Spartera CLI."""
import pytest
from unittest.mock import Mock, patch
import tempfile
import os
from pathlib import Path

@pytest.fixture
def mock_api_client():
    """Mock API client for testing."""
    with patch('spartera_cli.client.SparteraClient') as mock:
        yield mock

@pytest.fixture
def temp_config_dir():
    """Temporary config directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / '.spartera'
        config_dir.mkdir()
        
        with patch('spartera_cli.utils.config.get_config_dir', return_value=config_dir):
            yield config_dir

@pytest.fixture
def mock_env():
    """Mock environment variables."""
    env_vars = {
        'SPARTERA_API_KEY': 'test-api-key',
        'SPARTERA_COMPANY_ID': 'test-company-id',
        'SPARTERA_USER_ID': 'test-user-id'
    }
    
    with patch.dict(os.environ, env_vars):
        yield env_vars
'''
        (tests_path / "conftest.py").write_text(conftest_content)

        # test_cli.py
        test_cli_content = f'''"""Unit tests for CLI main functionality."""
import pytest
from typer.testing import CliRunner
from {self.config.package_name}.main import app

runner = CliRunner()

def test_cli_version():
    """Test CLI version command."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "{self.config.cli_name} version" in result.stdout

def test_cli_help():
    """Test CLI help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Spartera CLI" in result.stdout

def test_auth_commands_exist():
    """Test that auth commands are available."""
    result = runner.invoke(app, ["auth", "--help"])
    assert result.exit_code == 0
    assert "Authentication commands" in result.stdout

def test_asset_commands_exist():
    """Test that asset commands are available."""
    result = runner.invoke(app, ["asset", "--help"])
    assert result.exit_code == 0
    assert "Asset management" in result.stdout
'''
        (tests_path / "test_cli.py").write_text(test_cli_content)

    def _generate_docs(self, output_path: Path):
        """Generate documentation."""
        docs_path = output_path / "docs"

        # installation.md
        install_content = f"""# Installation Guide

## PyPI (Recommended)

```bash
pip install {self.config.package_name}
```

## From Source

```bash
git clone {self.config.github_url}
cd spartera-cli
pip install -e .
```

## Verification

```bash
{self.config.cli_name} --version
{self.config.cli_name} --help
```
"""
        (docs_path / "installation.md").write_text(install_content)

        # usage.md
        usage_content = f"""# Usage Guide

## Authentication

First, authenticate with your Spartera API key:

```bash
{self.config.cli_name} auth login
```

Get your API key from [app.spartera.com](https://app.spartera.com) → Settings → API Keys

## Basic Commands

### List Assets
```bash
{self.config.cli_name} asset list
{self.config.cli_name} asset list --format table
{self.config.cli_name} asset list --limit 10
```

### Process Assets
```bash
# Your private asset
{self.config.cli_name} process <asset-id>

# Marketplace asset
{self.config.cli_name} process company-handle/asset-slug

# Save results
{self.config.cli_name} process <asset-id> --output results.json

# Get visualization
{self.config.cli_name} process <asset-id> --svg --output chart.svg
```

## Output Formats

All commands support multiple output formats:

- `--format json` (default) - JSON output
- `--format table` - Pretty table output  
- `--format csv` - CSV output
"""
        (docs_path / "usage.md").write_text(usage_content)


def main():
    """Main function to generate CLI."""
    parser = argparse.ArgumentParser(
        description="Generate Spartera CLI from OpenAPI spec"
    )
    parser.add_argument(
        "--swagger", default="../../swagger.yaml", help="Path to swagger.yaml file"
    )
    parser.add_argument("--output", default="./spartera-cli", help="Output directory")
    parser.add_argument("--version", default="1.0.0", help="CLI version")

    args = parser.parse_args()

    print("🚀 Generating Spartera CLI...")
    print(f"📖 Swagger file: {args.swagger}")
    print(f"📁 Output: {args.output}")
    print(f"🏷️  Version: {args.version}")
    print()

    generator = SparteraCLIGenerator(args.swagger, args.version)
    generator.generate(args.output)


if __name__ == "__main__":
    main()
