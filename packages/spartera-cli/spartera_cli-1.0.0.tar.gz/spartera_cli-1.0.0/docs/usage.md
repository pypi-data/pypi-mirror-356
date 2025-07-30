# Usage Guide

## Authentication

First, authenticate with your Spartera API key:

```bash
spartera auth login
```

Get your API key from [app.spartera.com](https://app.spartera.com) → Settings → API Keys

## Basic Commands

### List Assets
```bash
spartera asset list
spartera asset list --format table
spartera asset list --limit 10
```

### Process Assets
```bash
# Your private asset
spartera process <asset-id>

# Marketplace asset
spartera process company-handle/asset-slug

# Save results
spartera process <asset-id> --output results.json

# Get visualization
spartera process <asset-id> --svg --output chart.svg
```

## Output Formats

All commands support multiple output formats:

- `--format json` (default) - JSON output
- `--format table` - Pretty table output  
- `--format csv` - CSV output
