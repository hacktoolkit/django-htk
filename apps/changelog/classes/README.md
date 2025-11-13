# Classes

Classes for parsing, storing, and formatting git changelog entries and release information.

## Imports

```python
from htk.apps.changelog.classes import (
    ChangeLog,
    LogEntry,
    ReleaseVersion,
)
```

## ChangeLog

Container for a git repository changelog with a list of log entries.

```python
changelog = ChangeLog(
    origin_url='https://github.com/owner/repo',
    log_entries=[log_entry1, log_entry2, ...]
)
```

### Fields

- `origin_url` - GitHub repository URL (e.g., `https://github.com/owner/repo`)
- `log_entries` - List of `LogEntry` objects

### Methods

#### write_changelog(changelog_file_name, slack_announce=False, slack_channel=None, slack_webhook_url=None, web_url=None)

Writes changelog to a markdown file and optionally announces to Slack.

```python
changelog.write_changelog(
    'CHANGELOG.md',
    slack_announce=True,
    slack_channel='#releases',
    slack_webhook_url='https://hooks.slack.com/...',
    web_url='https://example.com/changelog'
)
```

Parameters:
- `changelog_file_name` - Path to output markdown file
- `slack_announce` - Boolean to announce to Slack (default: False)
- `slack_channel` - Slack channel name (required if slack_announce=True)
- `slack_webhook_url` - Slack webhook URL for posting
- `web_url` - URL to changelog on the web (included in Slack message)

## LogEntry

Represents a single git commit log entry parsed from formatted git output.

```python
log_entry = LogEntry(
    origin_url='https://github.com/owner/repo',
    commit_hash='abc1234567...',
    date_iso='2024-01-15T10:30:00',
    author='john.doe',
    refs_raw='tag: v1.2.3, branch: main',
    subject='feat: add new feature (#123)'
)
```

### Fields

- `origin_url` - GitHub repository URL
- `commit_hash` - Full commit SHA-1 hash
- `date_iso` - ISO format date string
- `author` - Commit author username
- `refs_raw` - Raw git refs (tags, branches)
- `subject` - Commit message subject

### Factory Methods

#### from_line(origin_url, line)

Parse a LogEntry from a formatted git log line (fields separated by `SEPARATOR`).

```python
log_entry = LogEntry.from_line(
    'https://github.com/owner/repo',
    'abc1234567|john.doe|2024-01-15T10:30:00|tag: v1.2.3|feat: add feature (#123)'
)
```

### Properties

- `simple_subject` - Subject with GitHub issue references removed
- `issue_links` - Markdown-formatted GitHub issue links (e.g., `[#123](url)`)
- `issue_links_slack` - Slack-formatted issue links (e.g., `<url|#123>`)
- `author_github_url` - GitHub profile URL for the author
- `refs` - List of parsed git refs
- `release_version` - `ReleaseVersion` object if this is a release commit, None otherwise
- `is_release` - Boolean indicating if this commit is a release
- `url` - GitHub commit URL
- `short_date` - Formatted date as YYYY.MM.DD
- `html` - Markdown-formatted log entry (used in changelog files)
- `slack_message` - Slack-formatted log entry

### Methods

#### build_issue_links(fmt='markdown')

Build formatted issue links from GitHub issue references in the subject.

```python
# Markdown format
md_links = log_entry.build_issue_links(fmt='markdown')  # "[#123](url), [#124](url)"

# Slack format
slack_links = log_entry.build_issue_links(fmt='slack')  # "<url|#123>, <url|#124>"
```

Parameters:
- `fmt` - Format type: `'markdown'` or `'slack'`

## ReleaseVersion

Represents a release version parsed from a git tag reference.

```python
release = ReleaseVersion(
    origin_url='https://github.com/owner/repo',
    ref='tag: v1.2.3',
    date='20240115103000',
    sha='abc1234567',
    branch='main'
)
```

### Fields

- `origin_url` - GitHub repository URL
- `ref` - Git ref string (e.g., `tag: v1.2.3`)
- `date` - Release date in YYYYMMDDHHMMSS format
- `sha` - Commit SHA-1 hash
- `branch` - Git branch name

### Properties

- `readable_date` - Human-readable date format (e.g., `Mon Jan 15 10:30:00 2024`)
- `tag` - Extracted tag name (e.g., `v1.2.3`)
- `url` - GitHub release URL
