#!/usr/bin/env python
"""
Generate mkdocs navigation from README.md files in the htk directory structure.
This script scans the directory for README.md files and generates the appropriate
mkdocs navigation configuration dynamically.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any

def get_title_from_readme(path: Path) -> str:
    """Extract the first heading from a README file to use as title."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
    except Exception:
        pass
    return None

def format_name(dirname: str) -> str:
    """Convert directory name to readable format."""
    # Convert snake_case to Title Case
    words = dirname.replace('_', ' ').split()
    return ' '.join(word.capitalize() for word in words)

def build_nav_from_filesystem(base_path: Path, nav: List[Dict[str, Any]] = None, is_root: bool = True) -> List[Dict[str, Any]]:
    """
    Recursively build navigation from filesystem structure.
    Looks for README.md files and builds nested navigation.
    """
    if nav is None:
        nav = []

    # First, add standalone README.md files in this directory
    readme_path = base_path / 'README.md'
    if readme_path.exists() and not is_root:
        title = get_title_from_readme(readme_path)
        if not title:
            title = format_name(base_path.name)

        # Calculate relative path from docs directory
        try:
            rel_path = readme_path.relative_to(base_path.parent)
            # Convert to docs format: ../module/README.md -> module.md
            nav_path = str(rel_path).replace('README.md', '').rstrip('/') + '.md'
            nav_path = nav_path.replace('/', '')

            if nav_path:
                nav.append({title: nav_path})
        except ValueError:
            pass

    # Then, process subdirectories with their own README.md files
    subdirs = []
    try:
        for item in sorted(base_path.iterdir()):
            if item.is_dir() and not item.name.startswith(('.', '_', 'venv', '__pycache__', 'migrations', 'south_migrations', 'static', 'templates')):
                readme_exists = (item / 'README.md').exists()
                if readme_exists:
                    subdirs.append(item)
    except PermissionError:
        pass

    # Add subdirectories
    for subdir in subdirs:
        title = get_title_from_readme(subdir / 'README.md')
        if not title:
            title = format_name(subdir.name)

        rel_path = subdir / 'README.md'
        nav_path = f"{subdir.name}.md"
        nav.append({title: nav_path})

    return nav

def generate_mkdocs_nav(htk_base: Path) -> Dict[str, Any]:
    """Generate complete mkdocs navigation structure."""
    nav_config = []

    # Home
    nav_config.append({'Home': 'index.md'})

    # Top-level modules (direct children of htk/)
    top_level_modules = [
        'admin', 'admintools', 'api', 'cache', 'constants', 'data',
        'decorators', 'extensions', 'forms', 'middleware', 'models',
        'scripts', 'test_scaffold', 'templatetags', 'utils', 'validators'
    ]

    for module in top_level_modules:
        module_path = htk_base / module
        if (module_path / 'README.md').exists():
            title = get_title_from_readme(module_path / 'README.md')
            if not title:
                title = format_name(module)
            nav_config.append({title: f'{module}.md'})

    # Django Apps with submenu
    apps_path = htk_base / 'apps'
    if apps_path.exists():
        apps_nav = [{'Overview': 'apps.md'}]
        apps = sorted([d for d in apps_path.iterdir() if d.is_dir() and not d.name.startswith(('_', '__')) and (d / 'README.md').exists()])

        for app_dir in apps:
            title = get_title_from_readme(app_dir / 'README.md')
            if not title:
                title = format_name(app_dir.name)
            apps_nav.append({title: f'apps/{app_dir.name}.md'})

        nav_config.append({'Django Apps': apps_nav})

    # Libraries with submenu
    lib_path = htk_base / 'lib'
    if lib_path.exists():
        libs_nav = [{'Overview': 'lib.md'}]
        libs = sorted([d for d in lib_path.iterdir() if d.is_dir() and not d.name.startswith(('_', '__')) and (d / 'README.md').exists()])

        for lib_dir in libs:
            title = get_title_from_readme(lib_dir / 'README.md')
            if not title:
                title = format_name(lib_dir.name)
            libs_nav.append({title: f'lib/{lib_dir.name}.md'})

        nav_config.append({'Libraries': libs_nav})

    return nav_config

if __name__ == '__main__':
    # Find the htk directory
    script_dir = Path(__file__).parent
    htk_dir = script_dir.parent

    nav = generate_mkdocs_nav(htk_dir)

    # Print as YAML-like format for verification
    print("Navigation structure:")
    print("=" * 60)
    for i, item in enumerate(nav, 1):
        print(f"{i}. {list(item.keys())[0]}")

    print("\n✓ Navigation generated successfully")
    print(f"  Total items: {len(nav)}")
    sys.exit(0)
