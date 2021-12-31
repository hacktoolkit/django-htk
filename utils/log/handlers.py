# Python Standard Library Imports
import logging
import traceback

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
        exc_type, exc_value, exc_traceback = record.exc_info
        request = record.request
        reporter = ExceptionReporter(request, exc_type, exc_value, exc_traceback, is_email=True)

        try:
            exc = reporter.format_exception()
        except AttributeError:
            frames = reporter.get_traceback_frames()
            tb = [(f['filename'], f['lineno'], f['function'], f['context_line']) for f in frames]

            exc = ['Traceback (most recent call last):\n']
            exc += traceback.format_list(tb)
            exc += traceback.format_exception_only(exc_type, exc_value)

        message = '*%s* at `%s`\n\n```%s```' % (
            exc[-1].strip(),
            request.path_info,
            ''.join(exc[:-1]),
        )

        slack_debug(message)
