class ResponseError(Exception):
    """Generic ResponseError exception

    It helps to stop processing a view function by raising an exception.
    It is like `Http404` exception but with ability to define your response.

    NOTE: `htk.middleware.classes.CatchRaisedExceptionResponseMiddleware` MUST
          be in MIDDLEWARES in Django Settings.
    """

    def __init__(self, response):
        self.response = response
