from django.conf import settings

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

def resolve_method_dynamically(module_method_str):
    """Returns the method for a module

    `module_method_str` in the form of module.submodule.method
    """
    method = None
    if module_method_str:
        module_name = '.'.join(module_method_str.split('.')[:-1])
        method_name = module_method_str.split('.')[-1]
        if module_name and method_name:
            import sys
            method = getattr(sys.modules[module_name], method_name)
        else:
            pass
    else:
        pass
    return method
