from django.contrib.auth import logout

def logout_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
        return view_func(request, *args, **kwargs)
    return wrapped_view
