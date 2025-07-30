"""
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
