from django.conf import settings

from social.apps.django_app.middleware import SocialAuthExceptionMiddleware

class HtkSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        """Redirect to LOGIN_ERROR_URL by default
        Otherwise, go to the SOCIAL_AUTH_<STRATEGY>_LOGIN_ERROR_URL for that backend provider if specified

        However, if user is logged in when the exception occurred, it is a connection failure
        Therefore, always go to account settings page or equivalent
        """
        url = settings.LOGIN_ERROR_URL
        if request.user.is_authenticated():
            url = htk_setting('HTK_SOCIAL_AUTH_CONNECT_ERROR_URL', settings.LOGIN_ERROR_URL)
        else:
            url = super(HtkSocialAuthExceptionMiddleware, self).get_redirect_uri(request, exception)
        return url
