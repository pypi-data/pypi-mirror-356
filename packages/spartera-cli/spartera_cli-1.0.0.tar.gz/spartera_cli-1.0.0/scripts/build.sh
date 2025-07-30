#!/bin/bash
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
