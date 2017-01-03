from django.http import Http404

class MissingGoogleSiteVerificationFile(Http404):
    pass

class MissingHtmlSiteVerificationFile(Http404):
    pass

class MissingBingSiteVerificationFile(Http404):
    pass
