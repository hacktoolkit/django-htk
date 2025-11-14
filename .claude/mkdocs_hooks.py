"""
MkDocs hooks for dynamic README.md discovery and navigation generation.
This hook discovers all README.md files in the htk directory structure
and makes them available to mkdocs without requiring manual symlinks.
"""

import os
import shutil
from pathlib import Path
import logging

log = logging.getLogger('mkdocs.plugins')

def on_pre_build(config, **kwargs):
    """
    Pre-build hook to create necessary symbolic links from docs directory
    to actual README.md files across the codebase.
    This allows mkdocs to find and link to all READMEs dynamically.
    """
    docs_dir = Path(config['docs_dir'])
    htk_base = docs_dir.parent

    # Ensure docs/apps and docs/lib directories exist
    (docs_dir / 'apps').mkdir(exist_ok=True)
    (docs_dir / 'lib').mkdir(exist_ok=True)

    log.info("Creating symlinks for README files...")

    # Create symlinks for apps
    apps_dir = htk_base / 'apps'
    if apps_dir.exists():
        for app_path in sorted(apps_dir.iterdir()):
            if app_path.is_dir() and not app_path.name.startswith(('_', '__')):
                readme = app_path / 'README.md'
                if readme.exists():
                    symlink = docs_dir / 'apps' / f'{app_path.name}.md'
                    try:
                        if symlink.exists() or symlink.is_symlink():
                            symlink.unlink()
                        symlink.symlink_to(readme)
                        log.debug(f"Created symlink: {symlink.name}")
                    except Exception as e:
                        log.error(f"Failed to create symlink for {app_path.name}: {e}")

    # Create symlinks for libraries
    lib_dir = htk_base / 'lib'
    if lib_dir.exists():
        for lib_path in sorted(lib_dir.iterdir()):
            if lib_path.is_dir() and not lib_path.name.startswith(('_', '__')):
                readme = lib_path / 'README.md'
                if readme.exists():
                    symlink = docs_dir / 'lib' / f'{lib_path.name}.md'
                    try:
                        if symlink.exists() or symlink.is_symlink():
                            symlink.unlink()
                        symlink.symlink_to(readme)
                        log.debug(f"Created symlink: {symlink.name}")
                    except Exception as e:
                        log.error(f"Failed to create symlink for {lib_path.name}: {e}")

    log.info("Symlink generation complete")


def on_post_build(config, **kwargs):
    """
    Post-build hook to clean up temporary symlinks if needed.
    """
    log.info("Build complete - documentation ready")
