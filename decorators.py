import rollbar

from htk.middleware import GlobalRequestMiddleware
from htk.session_keys import DEPRECATED_ROLLBAR_NOTIFIED

def deprecated(func):
    """Decorator for reporting deprecated function calls

    Use this decorator sparingly, because we'll be charged if we make too many Rollbar notifications
    """
    def wrapped(*args, **kwargs):
        # try to get a request, may not always succeed
        request = GlobalRequestMiddleware.get_current_request()
        # notify a maximum of once per function per request/session
        if request:
            if DEPRECATED_ROLLBAR_NOTIFIED not in request.session:
                deprecated_notifications = {}
                request.session[DEPRECATED_ROLLBAR_NOTIFIED] = deprecated_notifications
            deprecated_notifications = request.session[DEPRECATED_ROLLBAR_NOTIFIED]
            key = '%s' % func
            # first get it
            already_notified = deprecated_notifications.get(key, False)
            # then mark it
            deprecated_notifications[key] = True
        else:
            already_notified = False

        if not already_notified:
            rollbar.report_message('Deprecated function call warning: %s' % func, 'warning', request)
        return func(*args, **kwargs)
    return wrapped
