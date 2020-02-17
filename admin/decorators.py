# Python Standard Library Imports
from functools import wraps

# Django Imports
from django.urls import reverse
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


class UsernameAdminProfileLinks(object):
    def __init__(self, user_resolver=None, short_description=None, admin_order_field=None):
        self.user_resolver = user_resolver
        self.short_description = short_description
        self.admin_order_field = admin_order_field

    def __call__(self, fn):
        @wraps(fn)
        def wrapped(instance, obj, *args, **kwargs):
            user = fn(instance, obj)

            if user:
                value = '<a href="%(admin_url)s">%(username)s</a> (<a href="%(profile_url)s" target="_blank">Profile</a>)' % {
                    'admin_url' : reverse('admin:auth_user_change', args=(user.id,)),
                    'username' : user.username,
                    'profile_url' : user.profile.get_absolute_url(),
                }
            else:
                value = '-'
            return mark_safe(value)

        if self.short_description:
            wrapped.short_description = self.short_description
        if self.admin_order_field:
            wrapped.admin_order_field = self.admin_order_field

        return wrapped
