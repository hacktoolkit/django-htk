# Future Imports
from __future__ import print_function

# Django Imports
from django.core.management.base import BaseCommand

# HTK Imports
from htk.apps.changelog.classes import (
    ChangeLog,
    LogEntry,
)
from htk.apps.changelog.utils import (
    fetch_git_logs,
    fetch_origin_url,
)
from htk.utils import htk_setting


class Command(BaseCommand):
    help = 'Updates CHANGELOG.md file'

    def add_arguments(self, parser):
        # Named (optional) argument
        parser.add_argument(
            '--slack-announce',
            action='store_true',
            default=False,
            dest='slack_announce',
            help='Announce release notes in Slack',
        )

    def handle(self, *args, **kwargs):

        # fetch log entries
        origin_url = fetch_origin_url()
        lines = fetch_git_logs()
        log_entries = LogEntry.from_lines(origin_url, lines)

        # Generate changelog
        changelog = ChangeLog(
            origin_url,
            log_entries,
            slack_announce=kwargs.get('slack_announce', False),
            slack_channel=htk_setting('HTK_CHANGELOG_SLACK_CHANNEL_RELEASES'),
            slack_full_log_message=htk_setting(
                'HTK_CHANGELOG_SLACK_FULL_LOG_MESSAGE'
            ),
        )
        changelog.write_changelog(
            changelog_file_name=htk_setting('HTK_CHANGELOG_FILE_PATH')
        )
