"""Unit tests for CLI main functionality."""
import pytest
from typer.testing import CliRunner
from spartera_cli.main import app

runner = CliRunner()

def test_cli_version():
    """Test CLI version command."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "spartera version" in result.stdout

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
