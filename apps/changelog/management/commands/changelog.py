# Future Imports
from __future__ import print_function

# Django Imports
from django.core.management.base import BaseCommand


# Django 1 and >2 compatible import
try:
    # Django Imports
    from django.urls import reverse
except ImportError:
    from django.urls import reverse

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
from htk.utils.urls import build_full_url


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
        parser.add_argument(
            '--silent',
            action='store_true',
            default=False,
            dest='silent',
            help='Run the command in silent',
        )

    def handle(self, *args, **kwargs):

        # fetch log entries
        origin_url = fetch_origin_url()
        lines = fetch_git_logs()
        log_entries = [LogEntry.from_line(origin_url, line) for line in lines]

        # Generate changelog
        changelog = ChangeLog(origin_url, log_entries)

        slack_announce = kwargs.get('slack_announce', False)
        silent = kwargs.get('silent', False)
        changelog_file_name = htk_setting('HTK_CHANGELOG_FILE_PATH')
        slack_channel = htk_setting('HTK_CHANGELOG_SLACK_CHANNEL_RELEASES')
        web_url_name = htk_setting('HTK_CHANGELOG_VIEW_IN_WEB_URL_NAME')
        web_url = htk_setting('HTK_CHANGELOG_VIEW_IN_WEB_URL')

        if web_url_name is not None:
            try:
                url = reverse(web_url_name)
                web_url = build_full_url(url, use_secure=True)
            except Exception:
                if not silent:
                    print(
                        'Given web URL name "{}" does not exist.'.format(
                            web_url_name
                        )
                    )
                exit()

        changelog.write_changelog(
            changelog_file_name=changelog_file_name,
            slack_announce=slack_announce,
            slack_channel=slack_channel,
            web_url=web_url,
        )

        if not silent:
            print('Change Log written to "{}".'.format(changelog_file_name))
            if slack_announce:
                print(
                    'Announcement is sent to "{}" channel in Slack'.format(
                        slack_channel
                    )
                )
