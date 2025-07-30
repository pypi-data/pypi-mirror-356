"""
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
