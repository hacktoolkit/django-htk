from django.conf import settings

def htk_setting(key, default=None):
    value = getattr(settings, key) if hasattr(settings, key) else default
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
