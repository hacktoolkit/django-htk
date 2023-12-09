# Python Standard Library Imports
from collections import namedtuple

# HTK Imports
from htk.compat import IS_PYTHON_2


# isort: off


class ChangeLog(
    namedtuple(
        'ChangeLog',
        'origin_url,log_entries',
    )
):
    # origin_url: str
    # log_entries: list[LogEntry]

    def write_changelog(
        self,
        changelog_file_name,
        slack_announce=False,
        slack_channel=None,
        slack_webhook_url=None,
        web_url=None,
    ):
        """Write Change Log to given file.

        It can announce the next release to slack.
        """
        buf = []
        slack_buf = [] if slack_announce else None
        most_recent_release = True

        for i, log_entry in enumerate(self.log_entries):
            # write header
            if i == 0 and not log_entry.is_release:
                buf.append('# Next Release')
                buf.append('')
                if slack_announce:
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
            if slack_announce and most_recent_release:
                slack_buf.append(log_entry.slack_message)

        # adds terminal newline
        buf.append('')

        with open(changelog_file_name, 'w') as f:
            string_to_write = '\n'.join(buf)
            if IS_PYTHON_2:
                string_to_write = string_to_write.encode('utf-8')
            else:
                # for Python 3, do nothing, as `.encode()` will convert to bytes
                pass
            f.write(string_to_write)

        if slack_announce:
            if slack_channel is None:
                raise Exception(
                    'Channel name must be provided to be able to post Slack'
                )

            from htk.lib.slack.utils import webhook_call as slack_webhook_call

            if web_url is not None:
                slack_buf.append('')
                slack_buf.append(
                    'The full log can be found at: {}'.format(web_url)
                )

            slack_message = '\n'.join(slack_buf)

            slack_webhook_call(
                webhook_url=slack_webhook_url,
                channel=slack_channel,
                text=slack_message,
                unfurl_links=False,
            )
