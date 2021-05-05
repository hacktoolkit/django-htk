# Python Standard Library Imports
import logging

# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.views.debug import ExceptionReporter

# HTK Imports
from htk.utils.debug import slack_debug


class RollbarHandler(logging.Handler):
    """An exception log handler that emits log entries to Rollbar
    """

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        exc_info = record.exc_info
        request = record.request
        rollbar.report_exc_info(exc_info=exc_info, request=request)


class SlackDebugHandler(logging.Handler):
    """An exception log handler that emits log entries to Slack
    """

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        exc_type, exc_value, traceback = record.exc_info
        request = record.request
        reporter = ExceptionReporter(request, exc_type, exc_value, traceback, is_email=True)

        exc = reporter.format_exception()

        message = '*%s* at `%s`\n\n```%s```' % (
            exc[-1].strip(),
            request.path_info,
            ''.join(exc[:-1]),
        )

        slack_debug(message)
