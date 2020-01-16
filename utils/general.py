# Python Standard Library Imports
import sys
from importlib import import_module

# Django Imports
from django.contrib import messages

# HTK Imports
from htk.utils.cache_descriptors import memoized


def htk_setting(key, default=None):
    from django.conf import settings
    import htk.constants.defaults
    if hasattr(settings, key):
        value = getattr(settings, key)
    elif default is not None:
        value = default
    elif hasattr(htk.constants.defaults, key):
        value = getattr(htk.constants.defaults, key)
    else:
        value = None
    return value


def get_module_name_parts(module_str):
    """Gets the name parts of a module string
    `module_str` in the form of module.submodule.method or module.submodule.class
    """
    if module_str:
        parts = module_str.split('.')
        module_name = '.'.join(parts[:-1])
        attr_name = parts[-1]
        values = (module_name, attr_name,)
    else:
        values = (None, None,)
    return values


@memoized
def resolve_method_dynamically(module_str):
    """Returns the method for a module
    """
    (module_name, attr_name,) = get_module_name_parts(module_str)
    if module_name and attr_name:
        module = import_module(module_name)
        method = getattr(module, attr_name)
    else:
        method = None
    return method


def _get_model_fn():
    try:
        from django.apps import apps
        get_model = apps.get_model
    except:
        from django.db.models.loading import get_model
    return get_model


def strtobool_safe(value):
    """Returns a `bool` based on `value`

    Wrapper around `distutils.util.strtobool`

    Returns `False` if any `Exception` occurs
    """
    try:
        from distutils.util import strtobool
        result = bool(strtobool(value))
    except:
        result = False
    return result


@memoized
def resolve_model_dynamically(module_str):
    (module_name, attr_name,) = get_module_name_parts(module_str)
    if module_name and attr_name:
        get_model = _get_model_fn()
        model = get_model(module_name, attr_name)
    else:
        model = None
    return model


def refresh(django_obj):
    refreshed = django_obj.__class__.objects.get(id=django_obj.id)
    return refreshed


def clear_messages(request):
    # clear messages by iterating
    # https://docs.djangoproject.com/en/1.11/ref/contrib/messages/#expiration-of-messages
    storage = messages.get_messages(request)
    for message in storage:
        pass
