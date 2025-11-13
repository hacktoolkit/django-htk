# Management

Django management commands for changelog operations.

## Available Commands

### changelog

Updates or generates a `CHANGELOG.md` file from git commit history.

```bash
python manage.py changelog
```

#### Options

- `--slack-announce` - Announce release notes to Slack channel (default: False)
- `--silent` - Suppress command output (default: False)
- `--help` - Show this help message and exit

#### Usage Examples

Generate changelog and write to file:
```bash
python manage.py changelog
```

Generate and announce to Slack:
```bash
python manage.py changelog --slack-announce
```

Run silently without output:
```bash
python manage.py changelog --silent
```

#### Configuration

The `changelog` command requires these Django settings:

- `HTK_CHANGELOG_FILE_PATH` - Path to output `CHANGELOG.md` file (required)
- `HTK_CHANGELOG_SLACK_CHANNEL_RELEASES` - Slack channel for announcements (e.g., `#releases`)
- `HTK_CHANGELOG_VIEW_IN_WEB_URL_NAME` - URL name for web changelog view (optional)
- `HTK_CHANGELOG_VIEW_IN_WEB_URL` - Direct URL to web changelog (optional, overridden by URL name)

#### Process

1. Fetches git commit logs from the repository
2. Parses commits into `LogEntry` objects
3. Identifies release commits based on git tags
4. Generates markdown-formatted changelog
5. Writes to file specified by `HTK_CHANGELOG_FILE_PATH`
6. If `--slack-announce` is set:
   - Sends formatted message to Slack channel
   - Includes link to full changelog if `HTK_CHANGELOG_VIEW_IN_WEB_URL` is configured

#### Example Output

The generated `CHANGELOG.md` includes:
- Release headers with dates and GitHub release links
- Commit entries with author, date, commit hash
- GitHub issue references linked to pull requests
- Formatted for both markdown and Slack presentation
