# Django Imports
from django.core.exceptions import AppRegistryNotReady

# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


# isort: off

try:
    PrelaunchSignup = resolve_model_dynamically(
        htk_setting('HTK_PRELAUNCH_MODEL')
    )
except (LookupError, AppRegistryNotReady):
    from htk.utils.debug import slack_debug

    slack_debug('AppRegistryNotReady: PrelaunchSignup loading failed')
    pass
