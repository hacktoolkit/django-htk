# Python Standard Library Imports
import datetime
from collections import namedtuple


class ReleaseVersion(
    namedtuple(
        'ReleaseVersion',
        'origin_url,ref,date,sha,branch',
    )
):
    # origin_url: str
    # ref: str
    # date: str
    # sha: str
    # branch: str

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
