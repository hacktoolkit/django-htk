# Django Imports
from django.http import HttpResponse
from htk.api.utils import json_response_error


class HttpErrorResponseError(Exception):
    """Generic Response Error exception

    It helps to stop processing a view function by raising an exception.
    It is like `Http404` exception but with ability to define your response.

    Status code defaults to 404 but can be overridden.

    NOTE: `htk.middleware.classes.HttpErrorResponseMiddleware` MUST be in
    MIDDLEWARES in Django Settings.
    """

    def __init__(self, response, status_code=404):
        if isinstance(response, str):
            self.response = json_response_error(
                {'message': response}, status=status_code
            )
        elif isinstance(response, dict):
            self.response = json_response_error(response, status=status_code)
        elif issubclass(response.__class__, HttpResponse):
            self.response = response
        else:
            raise TypeError(
                'response must be a string, dictionary or HttpResponse instance'
            )
