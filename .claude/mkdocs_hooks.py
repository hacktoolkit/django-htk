"""
MkDocs hooks for dynamic README.md discovery and navigation generation.
This hook discovers all README.md files in the htk directory structure
and makes them available to mkdocs without requiring manual symlinks.
"""

from pathlib import Path

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

    # Map of top-level directory names to documentation file names
    # This creates symlinks like: admin.md -> ../admin/README.md
    top_level_dirs = [
        'admin', 'admintools', 'api', 'cache', 'constants', 'decorators',
        'extensions', 'forms', 'middleware', 'models', 'utils', 'validators',
        'test_scaffold', 'scripts', 'templatetags'
    ]

    # Create symlinks for top-level modules
    for module_name in top_level_dirs:
        module_dir = htk_base / module_name
        if module_dir.exists() and module_dir.is_dir():
            readme = module_dir / 'README.md'
            if readme.exists():
                symlink = docs_dir / f'{module_name}.md'
                try:
                    if symlink.exists() or symlink.is_symlink():
                        symlink.unlink()
                    symlink.symlink_to(readme)
                except Exception as e:
                    pass

    # Create symlink for index.md from main README.md
    main_readme = htk_base / 'README.md'
    if main_readme.exists():
        index_symlink = docs_dir / 'index.md'
        try:
            if index_symlink.exists() or index_symlink.is_symlink():
                index_symlink.unlink()
            index_symlink.symlink_to(main_readme)
        except Exception as e:
            pass

    # Create symlinks for apps.md and lib.md overview files
    apps_readme = htk_base / 'apps' / 'README.md'
    if apps_readme.exists():
        apps_symlink = docs_dir / 'apps.md'
        try:
            if apps_symlink.exists() or apps_symlink.is_symlink():
                apps_symlink.unlink()
            apps_symlink.symlink_to(apps_readme)
        except Exception as e:
            pass

    lib_readme = htk_base / 'lib' / 'README.md'
    if lib_readme.exists():
        lib_symlink = docs_dir / 'lib.md'
        try:
            if lib_symlink.exists() or lib_symlink.is_symlink():
                lib_symlink.unlink()
            lib_symlink.symlink_to(lib_readme)
        except Exception as e:
            pass

    # Create symlinks for apps
    apps_dir = htk_base / 'apps'
    if apps_dir.exists():
        # Create top-level apps directory symlinks
        for top_module in ['apps', 'lib', 'utils', 'api', 'cache', 'forms', 'decorators', 'models', 'middleware', 'validators']:
            module_readme = htk_base / top_module / 'README.md'
            if module_readme.exists():
                symlink = docs_dir / top_module / 'README.md'
                symlink.parent.mkdir(exist_ok=True)
                try:
                    if symlink.exists() or symlink.is_symlink():
                        symlink.unlink()
                    symlink.symlink_to(module_readme)
                except Exception as e:
                    pass

        # Create symlinks for individual apps
        for app_path in sorted(apps_dir.iterdir()):
            if app_path.is_dir() and not app_path.name.startswith(('_', '__', 'README')):
                readme = app_path / 'README.md'
                if readme.exists():
                    symlink = docs_dir / 'apps' / f'{app_path.name}.md'
                    try:
                        if symlink.exists() or symlink.is_symlink():
                            symlink.unlink()
                        symlink.symlink_to(readme)
                    except Exception as e:
                        pass

    # Create symlinks for libraries
    lib_dir = htk_base / 'lib'
    if lib_dir.exists():
        for lib_path in sorted(lib_dir.iterdir()):
            if lib_path.is_dir() and not lib_path.name.startswith(('_', '__', 'README')):
                readme = lib_path / 'README.md'
                if readme.exists():
                    symlink = docs_dir / 'lib' / f'{lib_path.name}.md'
                    try:
                        if symlink.exists() or symlink.is_symlink():
                            symlink.unlink()
                        symlink.symlink_to(readme)
                    except Exception as e:
                        pass
