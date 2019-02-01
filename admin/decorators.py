# Python Standard Library Imports
from functools import wraps

# Third Party / PIP Imports

# Django Imports
from django.utils.safestring import mark_safe


def django_admin_bool_field(func):
    """Decorator for custom Django admin `bool` list fields to appear as a green check mark or red X
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        bool_value = func(*args, **kwargs)

        yes_icon = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
        no_icon = '<img src="/static/admin/img/icon-no.svg" alt="False">'

        value = yes_icon if bool_value else no_icon
        return mark_safe(value)
    return wrapped
