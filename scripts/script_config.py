# script_config.py
# shared settings for standalone scripts hooking into Django

import datetime
import inspect
import logging
import os
import re
import sys

sys.stdout = sys.stderr

SCRIPTS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.realpath(os.path.join(SCRIPTS_DIR, '..', '..').replace('\\', '/')))
sys.path.append(os.path.realpath(os.path.join(SCRIPTS_DIR, '..', '..', '..').replace('\\', '/')))

import django_settings_module
# Requires a django_settings_module.py at the project's top-level directory
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YOURAPP.settings')

# import rollbar so we can report stuff!
import rollbar

def job_runner(f):
    """Accepts any callable function and runs it

    Catches any exceptions and logs to Rollbar
    """
    try:
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
