# Third Party (PyPI) Imports
import dateparser
import emoji

# HTK Imports
from htk.apps.changelog.classes.release_version import ReleaseVersion
from htk.apps.changelog.constants.general import SEPERATOR
from htk.apps.changelog.constants.regexes import (
    GITHUB_ISSUE_REGEX,
    RELEASE_TAG_REGEXES,
)


class LogEntry:
    origin_url = ''
    commit_hash = ''
    date_iso = ''
    author = ''
    refs_raw = ''
    subject = ''
    sep = ''

    def __init__(
        self,
        origin_url,
        commit_hash='',
        date_iso='',
        author='',
        refs_raw='',
        subject='',
    ):
        self.origin_url = origin_url
        self.commit_hash = commit_hash
        self.date_iso = date_iso
        self.author = author
        self.refs_raw = refs_raw
        self.subject = subject

    @classmethod
    def from_line(cls, origin_url, line, sep=SEPERATOR):
        log_entry = cls(origin_url, *line.strip().split(sep))
        return log_entry

    @property
    def simple_subject(self):
        return GITHUB_ISSUE_REGEX.sub('', self.subject).strip()

    def build_issue_links(self, fmt='markdown'):
        """Returns a list of GitHUb Issue URLs

        fmt:
          - 'markdown': Markdown-formatted, comma-separated
          - 'slack': Slack-formatted
        """
        issues = GITHUB_ISSUE_REGEX.finditer(self.subject)

        def _format(issue):
            issue_num = issue.group("issue_num")
            issue_url = '{}/pull/{}'.format(
                self.origin_url, issue.group('issue_num')
            )
            if fmt == 'markdown':
                result = '[#{}]({})'.format(issue_num, issue_url)
            elif fmt == 'slack':
                result = '<{}|#{}>'.format(issue_url, issue_num)
            else:
                raise Exception('Unknown format: {}'.format(fmt))
            return result

        links = [_format(issue) for issue in issues]
        issue_links = ', '.join(links)
        return issue_links

    @property
    def issue_links(self):
        return self.build_issue_links(fmt='markdown')

    @property
    def issue_links_slack(self):
        return self.build_issue_links(fmt='slack')

    @property
    def refs(self):
        refs = [_.strip() for _ in self.refs_raw.split(',')]
        return refs

    @property
    def release_version(self):
        version = None
        for ref in self.refs:
            for regex in RELEASE_TAG_REGEXES:
                m = regex.match(ref)
                if m:
                    try:
                        version = ReleaseVersion(
                            origin_url=self.origin_url,
                            ref=ref,
                            date=m.group('dt'),
                            sha=m.group('sha'),
                            branch=m.group('branch'),
                        )
                    except Exception as ex:
                        print(ex)
                        # old format
                        # TODO: rewrite older tags to match the new format
                        version = ReleaseVersion(
                            origin_url=self.origin_url,
                            ref=ref,
                            date='{}{}'.format(m.group('date'), m.group('hms')),
                            sha='',
                            branch='',
                        )
                    break
            if version:
                break

        return version

    @property
    def is_release(self):
        return self.release_version is not None

    @property
    def url(self):
        url = '{}/commit/{}'.format(self.origin_url, self.commit_hash[:10])
        return url

    @property
    def short_date(self):
        dt = dateparser.parse(self.date_iso)
        value = dt.strftime('%Y.%m.%d')
        return value

    @property
    def html(self):
        simple_subject = emoji.demojize(self.simple_subject)
        issue_links = self.issue_links
        issue_links_sep = '; ' if issue_links else ''
        html = '- {} _by {} on {}_ ([{}]({}){}{})'.format(
            simple_subject,
            self.author,
            self.short_date,
            self.commit_hash[:10],
            self.url,
            issue_links_sep,
            issue_links,
        )
        return html

    @property
    def slack_message(self):
        issue_links = self.issue_links_slack
        issue_links_sep = '; ' if issue_links else ''
        html = '* {} _by {} on {}_ (<{}|{}>){}{}'.format(
            self.simple_subject,
            self.author,
            self.short_date,
            self.url,
            self.commit_hash[:10],
            issue_links_sep,
            issue_links,
        )
        return html
