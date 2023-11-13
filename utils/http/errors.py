class HttpErrorResponseError(Exception):
    """Generic Response Error exception

    It helps to stop processing a view function by raising an exception.
    It is like `Http404` exception but with ability to define your response.

    Status code defaults to 404 but can be overridden.

    NOTE: `htk.middleware.classes.HttpErrorResponseMiddleware` MUST be in
    MIDDLEWARES in Django Settings.
    """

    def __init__(self, response, status_code=None):
        self.response = response
        self.response.status_code = (
            status_code if status_code is not None else 404
        )
