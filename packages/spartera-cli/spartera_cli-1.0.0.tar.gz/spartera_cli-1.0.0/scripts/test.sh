#!/bin/bash
set -e

echo "🧪 Testing Spartera CLI..."

# Install in development mode
pip install -e .

# Basic functionality tests
spartera --version
spartera --help
spartera auth --help
spartera asset --help

echo "✅ Basic tests passed!"

# If API key is available, test API connectivity
if [ -n "$SPARTERA_API_KEY" ]; then
    echo "🔗 Testing API connectivity..."
    echo "$SPARTERA_API_KEY" | spartera auth login --stdin || true
    spartera auth status || true
else
    echo "⚠️  SPARTERA_API_KEY not set - skipping API tests"
fi
