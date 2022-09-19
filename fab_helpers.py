"""fab_helpers.py

Helper functions and classes for Fabric (http://fabric.readthedocs.org/en/latest/)
Used by fabfile.py
"""

# Python Standard Library Imports
import datetime

# Third Party (PyPI) Imports
import requests
from fabric.api import *


def tag_deploy():
    """Automatically create a tag whenever we deploy, so that we can roll-back to it at a future date"""
    commit_timestamp = local(
        'git log -n 1 --pretty=format:"%ct" master', capture=True
    )
    commit_datetimestr = datetime.datetime.utcfromtimestamp(
        float(commit_timestamp)
    ).strftime('%Y%m%d%H%M')
    revision = local('git log -n 1 --pretty=format:"%H" master', capture=True)
    local(
        'git tag -a deploy-{commit_datetimestr}-{revision}-master master -m "Auto-tagged deploy {commit_datetimestr} {revision}'.format(
            commit_datetimestr=commit_datetimestr,
            revision=revision[:10],
        )
    )
    local('git push --tags')


def rollbar_record_deploy(access_token, env='other'):
    """Tracking deploys
    http://rollbar.com/docs/deploys_fabric/
    """
    environment = env
    local_username = local('whoami', capture=True)
    # fetch last committed revision in the locally-checked out branch
    revision = local('git log -n 1 --pretty=format:"%H"', capture=True)

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
