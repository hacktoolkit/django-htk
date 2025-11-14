# Commands

Management commands for the changelog app.

## changelog

Updates or generates a `CHANGELOG.md` file from git commit history.

### Usage

```bash
python manage.py changelog [OPTIONS]
```

### Options

- `--slack-announce` - Announce release notes to Slack channel
- `--silent` - Suppress command output
- `--help` - Show help message

### Examples

```bash
# Generate changelog file
python manage.py changelog

# Generate and announce to Slack
python manage.py changelog --slack-announce

# Run silently
python manage.py changelog --silent
```

### Configuration Required

- `HTK_CHANGELOG_FILE_PATH` - Output file path for changelog
- `HTK_CHANGELOG_SLACK_CHANNEL_RELEASES` - Slack channel for announcements
- `HTK_CHANGELOG_VIEW_IN_WEB_URL_NAME` - Django URL name for web view (optional)
- `HTK_CHANGELOG_VIEW_IN_WEB_URL` - Direct changelog URL (optional)

### How It Works

1. Fetches git logs from repository
2. Parses commits using git log format
3. Creates `LogEntry` objects from each commit
4. Groups by releases (identifies tags)
5. Generates markdown-formatted changelog
6. Writes to `HTK_CHANGELOG_FILE_PATH`
7. Optionally announces to Slack with release notes
