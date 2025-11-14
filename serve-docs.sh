#!/bin/bash
# Serve script for local mkdocs development
# This script copies README files and serves the documentation locally

set -e

echo "Setting up documentation files..."

# Create docs directory
mkdir -p docs

# Copy README files with appropriate names
cp README.md docs/index.md
cp admin/README.md docs/admin.md
cp admintools/README.md docs/admintools.md
cp api/README.md docs/api.md
cp cache/README.md docs/cache.md
cp constants/README.md docs/constants.md
cp decorators/README.md docs/decorators.md
cp extensions/README.md docs/extensions.md
cp forms/README.md docs/forms.md
cp middleware/README.md docs/middleware.md
cp models/README.md docs/models.md
cp utils/README.md docs/utils.md
cp validators/README.md docs/validators.md
cp apps/README.md docs/apps.md
cp lib/README.md docs/lib.md
cp test_scaffold/README.md docs/test_scaffold.md
cp scripts/README.md docs/scripts.md
cp templatetags/README.md docs/templatetags.md

echo "✓ Documentation files copied"
echo ""
echo "Starting mkdocs server..."
mkdocs serve
