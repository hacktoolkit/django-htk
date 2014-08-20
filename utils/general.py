import sys

from importlib import import_module

from django.conf import settings
from django.db.models.loading import get_model

import htk.constants

def htk_setting(key, default=None):
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

def resolve_model_dynamically(module_str):
    (module_name, attr_name,) = get_module_name_parts(module_str)
    if module_name and attr_name:
        model = get_model(module_name, attr_name)
    else:
        model = None
    return model

def refresh(django_obj):
    refreshed = django_obj.__class__.objects.get(id=django_obj.id)
    return refreshed
