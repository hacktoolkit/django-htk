# Third Party (PyPI) Imports
import click

# HTK Imports
from htk.apps.changelog.classes import (
    ChangeLog,
    LogEntry,
)
from htk.apps.changelog.utils import (
    fetch_git_logs,
    fetch_origin_url,
)


@click.command()
@click.option(
    '--slack-announce/--no-slack-announce',
    default=False,
    help='Announce latest changes to Slack',
)
def update_changelog_command(slack_announce):
    origin_url = fetch_origin_url()
    lines = fetch_git_logs()
    log_entries = [LogEntry.from_line(origin_url, line) for line in lines]

    changelog = ChangeLog(origin_url, log_entries)

    changelog_file_name = './CHANGELOG.md'
    slack_channel = '#releases'

    changelog.write_changelog(
        changelog_file_name=changelog_file_name,
        slack_announce=slack_announce,
        slack_channel=slack_channel,
    )


if __name__ == '__main__':
    update_changelog_command()
