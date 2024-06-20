# Third Party (PyPI) Imports
from invoke import run

# HTK Imports
from htk.apps.changelog.constants.general import SEPARATOR
from htk.apps.changelog.constants.regexes import ORIGIN_URL_REGEX


def fetch_origin_url():
    """Fetch origin URL from GIT

    @return: str
    """
    command = 'git remote get-url origin'
    result = run(command, hide=True)

    raw_origin_url = result.stdout.strip()

    m = ORIGIN_URL_REGEX.match(raw_origin_url)

    origin_url = 'https://{}/{}/{}'.format(
        m.group('host'), m.group('org'), m.group('repository')
    )

    return origin_url


def fetch_git_logs():
    """Fetch git log in a specific format

    @return: list[str]
    """
    command = (
        'git log --mailmap --format="%H{SEP}%aI{SEP}%aN{SEP}%D{SEP}%s"'.format(
            SEP=SEPARATOR
        )
    )
    result = run(command, hide=True)

    lines = result.stdout.strip().split('\n')

    return lines
