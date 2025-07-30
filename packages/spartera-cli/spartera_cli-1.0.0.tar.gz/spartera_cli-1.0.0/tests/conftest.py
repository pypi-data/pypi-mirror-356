"""Test configuration for Spartera CLI."""
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
