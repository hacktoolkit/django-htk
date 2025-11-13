# Github

## Classes
- **`GitHubReminderBot`** (github/bots.py) - GitHub Reminder bot
- **`GitHubReminderCooldown`** (github/cachekeys.py) - Cache management object for not performing GitHub reminders for the same user too frequently
- **`BaseRelease`** (github/models/release.py) - Base model for GitHub releases.

## Functions
- **`pull_request_reminder`** (github/bots.py) - Returns a Markdown-formatted message for this organization's pull requests
- **`github_url`** (github/models/release.py) - Return the URL of the release.
- **`get_github_client`** (github/utils.py) - Get an authenticated GitHub client.
- **`get_repository`** (github/utils.py) - Get a GitHub repository by its full name.
- **`sync_release`** (github/utils.py) - Sync a single GitHub release to our database.
- **`sync_repository_releases`** (github/utils.py) - Sync all releases from a GitHub repository.
