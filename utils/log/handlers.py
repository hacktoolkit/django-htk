# Python Standard Library Imports
import logging
import traceback

# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.views.debug import ExceptionReporter

# HTK Imports
from apps.accounts.forms import settings
from utils.debug import slack_debug
from utils.general import htk_setting


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

    This handler routes error notifications to different Slack channels based on the environment:
    - Production: Sends to a configurable channel level (default: 'danger')
    - Development: Sends to the debug channel
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

        # Route to appropriate channel based on environment
        if settings.ENV_PROD:
            # Production: send to configurable channel level
            from utils.notifications import slack_notify

            # Get the production channel level from settings, default to 'danger' if not specified
            production_channel_level = htk_setting(
                'HTK_SLACK_PRODUCTION_ERROR_CHANNEL_LEVEL', 'danger'
            )

            slack_notify(message, level=production_channel_level)
        else:
            # Development: use debug channel
            slack_debug(message)
