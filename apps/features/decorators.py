# Python Standard Library Imports
from functools import wraps

# Django Imports
from django.http import HttpResponseForbidden

# HTK Imports
from htk.apps.features.utils import is_feature_enabled


class require_feature_enabled:
    def __init__(self, feature_name):
        self.feature_name = feature_name

    def __call__(self, view_fn):
        @wraps(view_fn)
        def wrapped(request, *args, **kwargs):
            if is_feature_enabled(self.feature_name):
                response = view_fn(request, *args, **kwargs)
            else:
                response = HttpResponseForbidden()
            return response

        return wrapped
