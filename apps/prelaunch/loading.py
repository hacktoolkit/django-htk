# Django Imports
from django.core.exceptions import AppRegistryNotReady

# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


try:
    PrelaunchSignup = resolve_model_dynamically(
        htk_setting('HTK_PRELAUNCH_MODEL')
    )
except (LookupError, AppRegistryNotReady):
    pass
