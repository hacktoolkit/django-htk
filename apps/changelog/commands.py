# Third Party (PyPI) Imports
import click

# HTK Imports
from htk.apps.changelog.classes import (
    ChangeLog,
    LogEntry,
)
from htk.apps.changelog.constants.defaults import HTK_CHANGELOG_SEP
from htk.apps.changelog.utils import (
    fetch_git_logs,
    fetch_origin_url,
)


# isort: off


@click.command()
@click.option(
    '--slack-announce/--no-slack-announce',
    default=False,
    help='Announce latest changes to Slack',
)
def update_changelog(slack_announce):
    origin_url = fetch_origin_url()
    lines = fetch_git_logs()
    log_entries = LogEntry.from_lines(origin_url, lines, HTK_CHANGELOG_SEP)

    changelog = ChangeLog(
        origin_url,
        log_entries,
        slack_announce=slack_announce,
    )
    changelog.write_changelog()
