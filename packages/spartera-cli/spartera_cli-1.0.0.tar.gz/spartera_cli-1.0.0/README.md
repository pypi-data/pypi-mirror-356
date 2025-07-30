# SPARTERA CLI

Official CLI for Spartera API platform

## 🚀 Installation

```bash
pip install spartera_cli
```

## 🔐 Authentication

```bash
spartera auth login
```

Get your API key from [app.spartera.com](https://app.spartera.com) → Settings → API Keys

## 📖 Quick Start

```bash
# List assets
spartera asset list

# Get asset details
spartera asset get <asset-id>

# Process an asset
spartera process <asset-id>

# Process marketplace asset
spartera process company-handle/asset-slug

# Save results to file
spartera process <asset-id> --output results.json

# Get SVG visualization
spartera process <asset-id> --svg --output chart.svg
```

## 📋 Commands

### Authentication
- `spartera auth login` - Authenticate with API key
- `spartera auth status` - Show current user info
- `spartera auth logout` - Clear credentials

### Assets
- `spartera asset list` - List assets
- `spartera asset get <id>` - Get asset details
- `spartera asset create` - Create asset
- `spartera asset delete <id>` - Delete asset

### Connections
- `spartera connection list` - List connections
- `spartera connection create` - Create connection
- `spartera connection test <id>` - Test connection

### Processing
- `spartera process <asset-ref>` - Process/analyze asset

### Output Formats
- `--format json|table|csv` - Output format
- `--output FILE` - Save to file

## 🛠️ Development

```bash
git clone https://github.com/spartera-com/spartera-cli
cd spartera-cli
pip install -e ".[dev]"
```

## 📞 Support

- **Issues**: [https://github.com/spartera-com/spartera-cli/issues](https://github.com/spartera-com/spartera-cli/issues)
- **Email**: tony@spartera.com
