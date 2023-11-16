# Django Imports
from django.http import HttpResponse


class HttpErrorResponseError(Exception):
    """Generic Response Error exception

    It helps to stop processing a view function by raising an exception.
    It is like `Http404` exception but with ability to define your response.

    Status code defaults to 404 but can be overridden if response is string.
    Status code is not changed if response is derived from `HttpResponse`.

    NOTE: `htk.middleware.classes.HttpErrorResponseMiddleware` MUST be in
    MIDDLEWARES in Django Settings.
    """

    def __init__(self, response, status_code=400):
        if status_code < 400 or status_code > 599:
            raise ValueError('Error status codes must be in 4xx or 5xx range')

        if isinstance(response, str):
            self.response = HttpResponse(response, status=status_code)
        elif issubclass(response.__class__, HttpResponse):
            self.response = response
            # replace any non-error status code with 4xx or 5xx errors
            if (
                self.response.status_code < 400
                or self.response.status_code > 599
            ):
                self.response.status_code = status_code
        else:
            raise TypeError(
                'response must be a string or HttpResponse instance'
            )
