from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

from htk.utils import htk_setting

def logged_in_redirect_home(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse(htk_setting('HTK_DEFAULT_LOGGED_IN_ACCOUNT_HOME')))
        return view_func(request, *args, **kwargs)
    return wrapped_view

def logout_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
        return view_func(request, *args, **kwargs)
    return wrapped_view

def requires_account_setup_completed(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            if not user.profile.has_completed_account_setup():
                return redirect('account_settings');
            else:
                pass
        else:
            pass
        return view_func(request, *args, **kwargs)
    return wrapped_view
