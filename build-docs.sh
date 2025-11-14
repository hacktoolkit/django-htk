#!/bin/bash
# Build script for mkdocs documentation
# Uses mkdocs hooks for dynamic README discovery and symlink generation
# See .claude/mkdocs_hooks.py for the hook implementation

set -e

echo "Building documentation site..."
echo "  • Hooks will auto-generate symlinks from README files"
echo "  • Documentation covers 90+ modules, 29 apps, and 44+ libraries"
echo ""

# Build the site
# The .claude/mkdocs_hooks.py hook will run before this and:
#   - Create symlinks for all top-level modules
#   - Create symlinks for all apps in apps/
#   - Create symlinks for all libraries in lib/
mkdocs build

echo "✓ Documentation built successfully"
echo "✓ Site output is in the 'site/' directory"
echo ""
echo "For local testing, run: mkdocs serve"
