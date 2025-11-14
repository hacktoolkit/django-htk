# Changelog App

Automatic changelog generation from Git history.

## Quick Start

```python
from htk.apps.changelog.utils import fetch_git_logs, fetch_origin_url

# Fetch git logs
logs = fetch_git_logs()

# Get repository origin
origin = fetch_origin_url()
```

## Common Patterns

```python
from htk.apps.changelog.classes.change_log import ChangeLog

# Write changelog
log = ChangeLog()
log.write_changelog('CHANGELOG.md')

# Build GitHub issue links
from htk.apps.changelog.classes.log_entry import LogEntry
entry = LogEntry('Fix: resolve bug #123')
links = entry.build_issue_links()  # ['https://github.com/owner/repo/issues/123']
```

## CLI

```bash
# Generate changelog from command line
python manage.py update_changelog
```

## Configuration

```python
# settings.py
CHANGELOG_FILE = 'CHANGELOG.md'
CHANGELOG_INCLUDE_TAGS = True
```
