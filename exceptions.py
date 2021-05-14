# Django Imports
from django.http import Http404


class AbstractMethodNotImplemented(Exception):
    pass


class MissingGoogleSiteVerificationFile(Http404):
    pass


class MissingHtmlSiteVerificationFile(Http404):
    pass


class MissingBingSiteVerificationFile(Http404):
    pass


class MissingBraveRewardsVerificationFile(Http404):
    pass
