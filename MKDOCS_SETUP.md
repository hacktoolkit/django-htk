# MkDocs Dynamic Documentation Setup

This documentation site uses a **scalable, dynamic approach** to handle README.md files across 29 apps and 44+ library integrations without requiring manual symlink maintenance.

## How It Works

### 1. MkDocs Hooks (``.claude/mkdocs_hooks.py``)

Before each build, mkdocs automatically executes the `on_pre_build` hook which:

- **Scans** the `htk/apps/` directory for README.md files
- **Scans** the `htk/lib/` directory for README.md files
- **Creates** temporary symlinks in `docs/apps/` and `docs/lib/` directories
- **Maps** each symlink to the corresponding README.md file

### 2. Dynamic Navigation (``mkdocs.yml``)

The `nav` configuration in `mkdocs.yml` references these dynamically-created symlinks:

```yaml
nav:
  - Django Apps:
      - Overview: apps.md
      - Accounts: apps/accounts.md      # Created dynamically by hook
      - Addresses: apps/addresses.md    # Created dynamically by hook
      - ... (all 29 apps)
  - Libraries:
      - Overview: lib.md
      - Airtable: lib/airtable.md       # Created dynamically by hook
      - ... (all 44+ libraries)
```

### 3. Why This Is Scalable

**Problem with manual symlinks:**
- Required manually creating symlinks for each new app/library
- Easy to forget when adding new modules
- Not maintainable as the codebase grows

**Solution with hooks:**
- ✅ Automatically detects all README.md files in apps/ and lib/
- ✅ Creates symlinks on-the-fly during each build
- ✅ No manual maintenance needed
- ✅ Symlinks are not committed to git (in .gitignore)
- ✅ New apps/libraries are automatically included

## Adding New Documentation

To add a new app or library to the documentation:

1. **Create a README.md** in your new app/library directory:
   ```
   htk/apps/my_new_app/README.md
   # My New App
   Description and documentation...
   ```

2. **Update mkdocs.yml** with the navigation entry:
   ```yaml
   nav:
     - Django Apps:
         - ... existing apps ...
         - My New App: apps/my_new_app.md  # Hook will create this symlink
   ```

3. **Build/serve** mkdocs:
   ```bash
   ./venv/bin/mkdocs serve
   ```

The hook will automatically create the symlink and include it in the build!

## Files Involved

- **`.claude/mkdocs_hooks.py`** - MkDocs hook that creates symlinks dynamically
- **`mkdocs.yml`** - Main configuration with hooks definition
- **`.gitignore`** - Ignores auto-generated `docs/apps/` and `docs/lib/` directories
- **`docs/extra.css`** - Custom styling (header color, footer behavior)

## Build Output

When building, you'll see:

```
INFO    -  Creating symlinks for README files...
INFO    -  Symlink generation complete
INFO    -  Documentation built in X.XX seconds
```

This confirms the hook is working and creating the necessary symlinks.

## Advantages

| Aspect | Manual Symlinks | Hook-based Approach |
|--------|---|---|
| Maintenance | High (manual) | None (automatic) |
| Scalability | Low | Excellent |
| New docs | Must add symlink | Automatic detection |
| Git tracking | Easy to forget | Never committed |
| Build time | N/A | < 1 second overhead |

