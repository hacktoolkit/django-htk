from social_django.middleware import SocialAuthExceptionMiddleware

from htk.utils import htk_setting

class HtkSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        """Redirect to LOGIN_ERROR_URL by default
        Otherwise, go to the SOCIAL_AUTH_<STRATEGY>_LOGIN_ERROR_URL for that backend provider if specified

        However, if user is logged in when the exception occurred, it is a connection failure
        Therefore, always go to account settings page or equivalent
        """
        default_url = super(HtkSocialAuthExceptionMiddleware, self).get_redirect_uri(request, exception)
        if request.user.is_authenticated():
            url = htk_setting('HTK_SOCIAL_AUTH_CONNECT_ERROR_URL', default_url)
        else:
            url = default_url
        return url
