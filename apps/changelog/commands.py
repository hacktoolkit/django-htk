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


def update_changelog_command_creator(slack_channel, changelog_file_name):
    """Update Changelog Command Creator

    Creates standalone CLI command tool to create/update change log file.

    Args:
        slack_channel       (str): Slack channel name with leading '#'
        changelog_file_name (str): Change log file name with relative or absolute file path.

    Usage:
        ```
        update_changelog_command = update_changelog_command_creator(
            '#releases',
            './CHANGELOG.md',
        )

        if __name__ == '__main__':
            update_changelog_command()
        ```
    """

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

        changelog.write_changelog(
            changelog_file_name=changelog_file_name,
            slack_announce=slack_announce,
            slack_channel=slack_channel,
        )

    return update_changelog_command


if __name__ == '__main__':
    # Example usage
    update_changelog_command = update_changelog_command_creator(
        '#releases', './CHANGELOG.md'
    )
    update_changelog_command()
