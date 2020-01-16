# Django Imports
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def company_officer_required(view_func):
    """Decorator for views that require access by company officer or staff user
    """
    @login_required
    def wrapped_view(request, *args, **kwargs):
        user = request.user
        if not(user.profile and user.profile.is_company_officer):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapped_view

def company_employee_required(view_func):
    """Decorator for views that require access by company employee or staff user
    """
    @login_required
    def wrapped_view(request, *args, **kwargs):
        user = request.user
        if not(user.profile and user.profile.is_company_employee):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapped_view
