# Django Imports
from django.http import HttpResponse


class HttpResponseAccepted(HttpResponse):
    status_code = 202


class ResponseError(Exception):
    """
    Generic ResponseError exception.
    """

    def __init__(self, response):
        self.response = response
