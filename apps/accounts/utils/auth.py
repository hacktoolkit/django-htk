from django.contrib.auth import login

def login_authenticated_user(request, authenticated_user):
    """Logs in an authenticated user and performs related updates
    `authenticated_user` has already been authenticated via one of the login backends
    """
    login(request, authenticated_user)
    authenticated_user.profile.update_locale_info_by_ip_from_request(request)
