"""
MkDocs hooks for dynamic README.md discovery and navigation generation.
This hook discovers all README.md files in the htk directory structure,
creates symbolic links, and dynamically generates the navigation config.
"""

from pathlib import Path


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


def generate_nav_config(htk_base: Path) -> list:
    """
    Generate complete mkdocs navigation structure from filesystem.
    Scans for README.md files and builds nested navigation dynamically.
    """
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
        apps = sorted([
            d for d in apps_path.iterdir()
            if d.is_dir() and not d.name.startswith(('_', '__'))
            and (d / 'README.md').exists()
        ])

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
        libs = sorted([
            d for d in lib_path.iterdir()
            if d.is_dir() and not d.name.startswith(('_', '__'))
            and (d / 'README.md').exists()
        ])

        for lib_dir in libs:
            title = get_title_from_readme(lib_dir / 'README.md')
            if not title:
                title = format_name(lib_dir.name)
            libs_nav.append({title: f'lib/{lib_dir.name}.md'})

        nav_config.append({'Libraries': libs_nav})

    return nav_config


def create_symlinks(docs_dir: Path, htk_base: Path):
    """
    Create necessary symbolic links from docs directory to actual README.md files.
    This allows mkdocs to find all READMEs dynamically.
    """
    # Ensure docs/apps and docs/lib directories exist
    (docs_dir / 'apps').mkdir(exist_ok=True)
    (docs_dir / 'lib').mkdir(exist_ok=True)

    # Map of top-level directory names to documentation file names
    # This creates symlinks like: admin.md -> ../admin/README.md
    top_level_dirs = [
        'admin', 'admintools', 'api', 'cache', 'constants', 'data', 'decorators',
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
                except Exception:
                    pass

    # Create symlink for index.md from main README.md
    main_readme = htk_base / 'README.md'
    if main_readme.exists():
        index_symlink = docs_dir / 'index.md'
        try:
            if index_symlink.exists() or index_symlink.is_symlink():
                index_symlink.unlink()
            index_symlink.symlink_to(main_readme)
        except Exception:
            pass

    # Create symlinks for apps.md and lib.md overview files
    apps_readme = htk_base / 'apps' / 'README.md'
    if apps_readme.exists():
        apps_symlink = docs_dir / 'apps.md'
        try:
            if apps_symlink.exists() or apps_symlink.is_symlink():
                apps_symlink.unlink()
            apps_symlink.symlink_to(apps_readme)
        except Exception:
            pass

    lib_readme = htk_base / 'lib' / 'README.md'
    if lib_readme.exists():
        lib_symlink = docs_dir / 'lib.md'
        try:
            if lib_symlink.exists() or lib_symlink.is_symlink():
                lib_symlink.unlink()
            lib_symlink.symlink_to(lib_readme)
        except Exception:
            pass

    # Clean up old directory-level README.md symlinks that shouldn't exist
    # (We use top-level .md symlinks instead)
    old_dirs = ['api', 'cache', 'decorators', 'forms', 'middleware', 'models', 'utils', 'validators']
    for dir_name in old_dirs:
        old_readme = docs_dir / dir_name / 'README.md'
        if old_readme.exists() or old_readme.is_symlink():
            try:
                old_readme.unlink()
            except Exception:
                pass

    # Create symlinks for apps
    apps_dir = htk_base / 'apps'
    if apps_dir.exists():
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
                    except Exception:
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
                    except Exception:
                        pass


def on_pre_build(config, **kwargs):
    """
    Pre-build hook to create symlinks and dynamically generate navigation.
    This ensures mkdocs has access to all README.md files and the nav is always in sync.
    """
    docs_dir = Path(config['docs_dir'])
    htk_base = docs_dir.parent

    # Create all necessary symlinks
    create_symlinks(docs_dir, htk_base)

    # Generate and set dynamic navigation config
    config['nav'] = generate_nav_config(htk_base)
