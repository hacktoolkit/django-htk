# Python Standard Library Imports
import datetime
import hashlib
import json

# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.contrib.auth import login

# HTK Imports
from htk.apps.accounts.utils import encrypt_uid
from htk.apps.accounts.utils import resolve_encrypted_uid
from htk.compat import b64decode, b64encode
from htk.utils import htk_setting
from htk.utils import utcnow
from htk.utils.datetime_utils import datetime_to_unix_time
from htk.utils.datetime_utils import unix_time_to_datetime


def login_authenticated_user(request, authenticated_user, backend=None):
    """Logs in an authenticated user and performs related updates
    `authenticated_user` has already been authenticated via one of the login backends
    """
    login(request, authenticated_user, backend=backend)
    authenticated_user.profile.update_locale_info_by_ip_from_request(request)

    if htk_setting('HTK_ITERABLE_ENABLED'):
        try:
            from htk.lib.iterable.utils import get_iterable_api_client
            itbl = get_iterable_api_client()
            itbl.notify_login(authenticated_user)
        except:
            rollbar.report_exc_info()


def get_user_token_auth_token(user, expires_minutes=None):
    """Returns the token to auth/log in the `user`

    Typically would want to include the generated token in an email
    so that that user can directly log in to the app.
    """
    encrypted_uid = encrypt_uid(user)

    expires_minutes = expires_minutes if expires_minutes else htk_setting('HTK_USER_TOKEN_AUTH_EXPIRES_MINUTES')
    expires = utcnow() + datetime.timedelta(minutes=expires_minutes)
    expires_timestamp = datetime_to_unix_time(expires)

    hashed = get_user_token_auth_hash(user, expires_timestamp)

    data = {
        'user' : encrypted_uid,
        'expires' : expires_timestamp,
        'hash' : hashed,
    }

    token = b64encode(json.dumps(data))
    return token


def get_user_token_auth_hash(user, expires_timestamp):
    """Generates the hash portion of a user token-auth token
    """
    encrypted_uid = encrypt_uid(user)
    salt = user.profile.salt
    key = htk_setting('HTK_USER_TOKEN_AUTH_ENCRYPTION_KEY')

    prehash = '%s|%s|%s|%s' % (
        encrypted_uid,
        salt,
        expires_timestamp,
        key,
    )

    hashed = hashlib.sha256(prehash.encode()).hexdigest()

    return hashed


def validate_user_token_auth_token(token):
    """Validates a user token-auth token

    Returns a 2-tuple of `(user, is_valid,)`

    Defaults to `(None, False,)`
    """
    user = None
    is_valid = False

    try:
        data = json.loads(b64decode(token))
    except ValueError:
        data = None

    if data is not None:
        # verify expiration of token

        expires_timestamp = data.get('expires', 0)
        expires = unix_time_to_datetime(expires_timestamp)

        if expires > utcnow():
            # token has not expired

            encrypted_uid = data.get('user', -1)
            user = resolve_encrypted_uid(encrypted_uid)

            if user:
                # found a matching user
                # verify hash

                received_hash = data.get('hash', None)
                expected_hash = get_user_token_auth_hash(user, expires_timestamp)

                if received_hash == expected_hash:
                    # hash matches
                    is_valid = True
                else:
                    # hash does not match
                    user = None
            else:
                # no user found
                pass

        else:
            # token has expired
            pass

    return (user, is_valid,)
