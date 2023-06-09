# Python Standard Library Imports
import re

# Third Party (PyPI) Imports
import requests
from requests.auth import HTTPBasicAuth

# Django Imports
from django.conf import settings

# HTK Imports
from htk.utils.regex import RE


class RabbitMQAPIClient(object):
    BROKER_URL_PATTERN = re.compile('^amqps://(?P<username>[a-z]+):(?P<password>[A-Za-z0-9_]+)@(?P<host>[A-Za-z0-9-.]+)/(?P<username2>[a-z]+)$')

    def __init__(self):
        if RE.match(self.BROKER_URL_PATTERN, settings.CELERY_BROKER_URL):
            self.username = RE.m.group('username')
            self.password = RE.m.group('password')
            self.host = RE.m.group('host')
        else:
            raise Exception('Was not able to initialize RabbitMQ connection. Is CELERY_BROKER_URL set correctly?')

    def get_queues(self):
        resource = 'api/queues'
        url = 'https://{}/{}'.format(self.host, resource)
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
        return response.json()
