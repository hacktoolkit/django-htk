# Changelog

This app helps to create CHANGELOG.md file containing Release Notes


## Installation

### PyPI Packages
Install the PyPI packages in `requirements.txt`

### Adding to Installed Apps
Add `htk.apps.changelog` to `INSTALLED_APPS` in `settings.py`

### Setting up options
There are 3 constants can be set in `settings.py` file.

- `HTK_CHANGELOG_FILE_PATH`: File path for CHANGELOG.md file.
  Default: `CHANGELOG.md`
- `HTK_CHANGELOG_SLACK_CHANNEL`: Slack channel name to announce.
  Default: `#release-notes`
- `HTK_CHANGELOG_SLACK_FULL_LOG_MESSAGE`: The message that will show at the end of the thread.
  Default: `The full change log can be found at CHANGELOG.md`

### Views
Not necessary but app allows to list release notes as a page.
Create a view function and pass the necessary content to app's view function:

```python
def changelog(request):
    from htk.apps.changelog.views import changelog_view
    response = changelog_view(request, 'app/changelog.html', {}, render)
    return response
```

In template file predefined template fragment can be used:

```
{% include 'htk/fragments/changelog/view.html' with changelog=changelog %}
```


## Usage
This app adds a new command to `manage.py`. It can be used with following command:

```bash
venv/bin/python manage.py changelog
```

If slack announcement wanted `--slack-announce` can be passed to command:

```bash
venv/bin/python manage.py changelog --slack-announce
```

### Direct Command Tool
There is an alternative way to add command tool if Django command is not choosen.
There is an example in `commands.py` for usage.
