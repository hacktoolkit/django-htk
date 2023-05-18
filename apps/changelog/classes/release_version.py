# Python Standard Library Imports
import datetime


class ReleaseVersion:
    origin_url = ''
    ref = ''
    date = ''
    sha = ''
    branch = ''

    def __init__(self, origin_url, ref='', date='', sha='', branch=''):
        self.origin_url = origin_url
        self.ref = ref
        self.date = date
        self.sha = sha
        self.branch = branch

    @property
    def readable_date(self):
        dt = datetime.datetime.strptime(self.date, '%Y%m%d%H%M%S')

        # fmt = '%A, %B %-d, %Y %H:%M%S'
        fmt = '%c'
        value = dt.strftime(fmt) if dt else self.date
        return value

    @property
    def tag(self):
        value = (
            self.ref[len('tag: ') :]  # noqa: E203
            if self.ref.startswith('tag: ')
            else self.ref
        )
        return value

    @property
    def url(self):
        url = '{}/releases/tag/{}'.format(self.origin_url, self.tag)
        return url
