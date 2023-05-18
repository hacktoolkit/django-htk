# HTK Imports
from htk.apps.changelog.constants.defaults import (
    HTK_CHANGELOG_SLACK_CHANNEL_RELEASES,
    HTK_CHANGELOG_SLACK_FULL_LOG_MESSAGE,
)


# isort: off


class ChangeLog:
    def __init__(
        self,
        origin_url,
        log_entries,
        slack_announce=False,
        slack_channel=HTK_CHANGELOG_SLACK_CHANNEL_RELEASES,
        slack_full_log_message=HTK_CHANGELOG_SLACK_FULL_LOG_MESSAGE,
    ):
        self.origin_url = origin_url
        self.log_entries = log_entries
        self.slack = {
            'announce': slack_announce,
            'channel': slack_channel,
            'full_log_message': slack_full_log_message,
        }

    def write_changelog(self, changelog_file_name='CHANGELOG.md'):
        buf = []
        slack_buf = [] if self.slack['announce'] else None
        most_recent_release = True

        for i, log_entry in enumerate(self.log_entries):
            # write header
            if i == 0 and not log_entry.is_release:
                buf.append('# Next Release')
                buf.append('')
                if self.slack['announce']:
                    slack_buf.append('*Most Recent Release*')
                    slack_buf.append('')
            elif log_entry.is_release:
                if i > 0:
                    most_recent_release = False
                release_version = log_entry.release_version
                buf.append('')
                buf.append(
                    '# Release: {} ([{}]({}))'.format(
                        release_version.readable_date,
                        release_version.tag,
                        release_version.url,
                    )
                )
                buf.append('')
            else:
                pass

            # write log entry
            buf.append(log_entry.html)
            if self.slack['announce'] and most_recent_release:
                slack_buf.append(log_entry.slack_message)

        # adds terminal newline
        buf.append('')

        with open(changelog_file_name, 'w') as f:
            f.write('\n'.join(buf))

        if self.slack['announce']:
            from htk.lib.slack.utils import webhook_call as slack_webhook_call

            slack_buf.append('')
            slack_buf.append(self.slack['full_log_message'])
            slack_message = '\n'.join(slack_buf)

            slack_webhook_call(
                channel=self.slack['channel'],
                text=slack_message,
                unfurl_links=False,
            )
