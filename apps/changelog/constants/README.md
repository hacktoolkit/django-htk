# Changelog Constants

## Overview

This module defines configuration for parsing and processing changelog files, including regex patterns for release tags, GitHub issues, and repository URLs.

## Constants

### Configuration Settings

- **`HTK_CHANGELOG_FILE_PATH`** - Default: `'CHANGELOG.md'` - Path to changelog file
- **`HTK_CHANGELOG_SLACK_CHANNEL_RELEASES`** - Default: `'#release-notes'` - Slack channel for release notifications
- **`HTK_CHANGELOG_VIEW_IN_WEB_URL_NAME`** - Default: `None` - URL name for changelog view (optional)
- **`HTK_CHANGELOG_VIEW_IN_WEB_URL`** - Default: `None` - Direct URL to changelog (optional)
- **`HTK_COMPANY_EMPLOYEE_GITHUB_USERNAMES_MAP`** - Default: `{}` - Map GitHub usernames to employee names

### Regex Patterns

- **`RELEASE_TAG_REGEXES`** - List of compiled regexes for parsing release tags:
  - New format: `tag: deploy-202211031730-4acb099a93-master`
  - Old format: `tag: deploy-20220710.195443`
- **`GITHUB_ISSUE_REGEX`** - Pattern matching GitHub issue references: `(#123)`
- **`ORIGIN_URL_REGEX`** - Pattern matching Git origin URLs: `git@github.com:org/repo.git`

## Usage Examples

### Parse Release Tags

```python
import re
from htk.apps.changelog.constants import RELEASE_TAG_REGEXES

tag = 'tag: deploy-202211031730-4acb099a93-master'
for pattern in RELEASE_TAG_REGEXES:
    match = pattern.match(tag)
    if match:
        print(f"Date: {match.group('dt')}, SHA: {match.group('sha')}")
        break
```

### Extract GitHub Issues

```python
from htk.apps.changelog.constants import GITHUB_ISSUE_REGEX

text = 'Fixed bug (#123) and improved feature (#456)'
for match in GITHUB_ISSUE_REGEX.finditer(text):
    print(f"Issue: #{match.group('issue_num')}")
```

### Parse Repository URL

```python
from htk.apps.changelog.constants import ORIGIN_URL_REGEX

url = 'git@github.com:hacktoolkit/django.git'
match = ORIGIN_URL_REGEX.match(url)
if match:
    print(f"Org: {match.group('org')}, Repo: {match.group('repository')}")
```

### Configure Settings

```python
# In Django settings.py
HTK_CHANGELOG_FILE_PATH = 'docs/CHANGELOG.md'
HTK_CHANGELOG_SLACK_CHANNEL_RELEASES = '#deployments'
HTK_COMPANY_EMPLOYEE_GITHUB_USERNAMES_MAP = {
    'john_doe': 'John Doe',
    'jane_smith': 'Jane Smith',
}
```
