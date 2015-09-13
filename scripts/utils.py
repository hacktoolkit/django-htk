import rollbar

from htk.utils.db import ensure_mysql_connection_usable

def job_runner(f):
    """Accepts any callable function and runs it

    Catches any exceptions and logs to Rollbar
    """
    try:
        ensure_mysql_connection_usable()
        f()
    except:
        rollbar.report_exc_info()

def slog(m, level='info'):
    logger = logging.getLogger(__name__)
    logger_fns = {
        'debug' : logger.debug,
        'info' : logger.info,
        'warning' : logger.warn,
        'error' : logger.error,
        'critical' : logger.critical,
    }
    logger_fn = logger_fns.get(level, logger.info)

    previous_call = inspect.stack()[1]
    previous_fn = previous_call[0].f_code.co_name
    previous_file = previous_call[1]
    extra = {
        'file' : previous_file,
        'func' : previous_fn,
    }
    logger_fn(m, extra=extra)
