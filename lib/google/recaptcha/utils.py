# Python Standard Library Imports

# Third Party / PIP Imports
import requests

# Django Imports

# HTK Imports
from htk.lib.google.recaptcha.constants import GOOGLE_RECAPTCHA_API_SITE_VERIFY_URL
from htk.utils import htk_setting


def google_recaptcha_site_verification(response_token, remote_ip=None):
    """Gets verification data on a Google Recaptcha response token

    The response is a JSON object:

    {
      "success": true|false,
      "challenge_ts": timestamp,  // timestamp of the challenge load (ISO format yyyy-MM-dd'T'HH:mm:ssZZ)
      "hostname": string,         // the hostname of the site where the reCAPTCHA was solved
      "error-codes": [...]        // optional
    }

    https://developers.google.com/recaptcha/docs/verify#api_request
    """
    data = {
        'secret' : htk_setting('HTK_GOOGLE_RECAPTCHA_SECRET_KEY'),
        'response' : response_token,
        'remoteip' : remote_ip,
    }
    response = requests.post(
        GOOGLE_RECAPTCHA_API_SITE_VERIFY_URL,
        data=data
    )

    response_json = response.json()
    return response_json
