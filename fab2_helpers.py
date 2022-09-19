"""fab_helpers.py

Helper functions and classes for Fabric (https://docs.fabfile.org/en/latest/)
Used by fabfile.py
"""

# Python Standard Library Imports
import datetime

# Third Party (PyPI) Imports
import requests
from fabric.util import get_local_user


def tag_deploy(conn):
    """Automatically create a tag whenever we deploy, so that we can roll-back to it at a future date"""
    result = conn.local('git log -n 1 --pretty=format:"%ct" master', hide=True)
    commit_timestamp = result.stdout.splitlines()[-1]
    commit_datetimestr = datetime.datetime.utcfromtimestamp(
        float(commit_timestamp)
    ).strftime('%Y%m%d%H%M')

    result = conn.local('git log -n 1 --pretty=format:"%H" master', hide=True)
    revision = result.stdout.splitlines()[-1]

    conn.local(
        f'git tag -a deploy-{commit_datetimestr}-{revision[:10]}-master master -m "Auto-tagged deploy {commit_datetimestr} {revision}"',
        hide=True,
        warn=True,
    )

    conn.local('echo $SSH_AUTH_SOCK')  # TODO: temporary debugging
    conn.local('git push --tags', hide=True, warn=True)
    # TODO: manually run for now
    conn.local('echo Run locally: git push --tags')


def rollbar_record_deploy(conn, access_token, env='other'):
    """Tracking deploys
    http://rollbar.com/docs/deploys_fabric/
    """
    environment = env
    local_username = get_local_user()

    # fetch last committed revision in the locally-checked out branch
    result = conn.local('git log -n 1 --pretty=format:"%H"')
    revision = result.stdout.splitlines()[-1]

    resp = requests.post(
        'https://api.rollbar.com/api/1/deploy/',
        {
            'access_token': access_token,
            'environment': environment,
            'local_username': local_username,
            'revision': revision,
        },
        timeout=3,
    )

    if resp.status_code == 200:
        print("Deploy recorded successfully.")
    else:
        print("Error recording deploy:", resp.text)


class AbstractFabricTaskManager(object):
    def deploy(self):
        """Default deploy task"""
        print('I am a dummy task')

    def _get_hosts(self):
        hosts = []
        return hosts

    def _get_setup_args(self):
        setup_args = '-h'
        return setup_args
