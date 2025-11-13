# GitHub Integration

Repository management and release tracking.

## Quick Start

```python
from htk.lib.github.utils import get_repository, sync_repository_releases

repo = get_repository('owner/repo')
sync_repository_releases(repo)
```

## Bots & Reminders

```python
from htk.lib.github.bots import GitHubReminderBot

bot = GitHubReminderBot()
reminder = bot.pull_request_reminder(org)
```

## Configuration

```python
# settings.py
GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN')
```
