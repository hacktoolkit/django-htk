# Python Standard Library Imports
import base64
import hashlib
import time
import typing as T

# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.http import HttpRequest
from django.utils.http import (
    base36_to_int,
    int_to_base36,
)

# HTK Imports
from htk.apps.accounts.constants import (
    EMAIL_TO_USERNAME_HASH_LENGTH,
    USERNAME_MAX_LENGTH,
)
from htk.apps.accounts.exceptions import NonUniqueEmail
from htk.compat import (
    b64encode,
    uuid4_hex,
)
from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically
from htk.utils.request import get_current_request
from htk.validators import is_valid_email


# isort: off


##
# model resolvers


def get_user_profile_model():
    user_profile_model_name = htk_setting('HTK_USER_PROFILE_MODEL')
    UserProfileModel = resolve_model_dynamically(user_profile_model_name)
    return UserProfileModel


##
# login and registration


def create_user(
    first_name, last_name, email, username_prefix=None, set_password=True
):
    """Creates a new user

    Side Effects:
    - Associates User with UserEmail
    - Sets password if `set_password` is `True`
    """

    UserModel = get_user_model()

    if username_prefix and isinstance(username_prefix, str):
        username = '%s_%s' % (
            username_prefix,
            uuid4_hex()[:10],
        )
    else:
        username = email_to_username_pretty_unique(email)

    user = UserModel.objects.create(
        username=username, first_name=first_name, last_name=last_name
    )

    # associate user email and sets primary email
    user_email = associate_user_email(user, email, confirmed=True)
    user_email.set_primary_email()

    if set_password:
        password = set_random_password(user)
    else:
        password = None

    return user, password


def set_random_password(user, password_length=16):
    """Sets a random password for `user`

    Utilizes hex UUID
    """
    password = uuid4_hex()[:password_length]
    user.set_password(password)
    user.save()
    return password


def email_to_username_hash(email):
    """Convert emails to hashed versions where we store them in the username field
    We can't just store them directly, or we'd be limited to Django's username <= 30
    chars limit, which is really too small for arbitrary emails

    From: https://github.com/dabapps/django-email-as-username/blob/master/emailusernames/utils.py  # noqa: E501
    """
    # Emails should be case-insensitive unique
    email = email.lower()
    # Deal with internationalized email addresses
    converted = email.encode('utf8', 'ignore')
    hashed = b64encode(hashlib.sha256(converted).hexdigest(), url_safe=True)[
        :EMAIL_TO_USERNAME_HASH_LENGTH
    ]
    return hashed


def email_to_username_pretty_unique(email):
    """Converts `email` to a pretty and unique username based on the email

    To be efficient, only do one DB check for pre-existing username
    """
    from htk.utils.emails import extract_snowflake_handle_from_email

    handle = extract_snowflake_handle_from_email(email).replace('.', '_')
    username = handle[:USERNAME_MAX_LENGTH]
    user = get_user_by_username(username)
    if user:
        # need to append some hashed chars to it to make a unique username
        hashed = email_to_username_hash(email)
        if len(username) < USERNAME_MAX_LENGTH:
            pad_length = USERNAME_MAX_LENGTH - (len(username) + 1)
            username = username + '_' + hashed[:pad_length]
        else:
            username = hashed
    else:
        pass
    return username


def get_user_by_username(username, UserModel=None):
    """Gets a user by `username`

    Returns None if not found
    """
    if UserModel is None:
        UserModel = get_user_model()

    try:
        user = UserModel.objects.get(username=username)
    except UserModel.DoesNotExist:
        user = None
    return user


def get_user_by_email(email):
    """Gets a User by `email`
    Returns None if not found
    """
    from htk.apps.accounts.models import UserEmail

    if is_valid_email(email):
        # check for confirmed email addresses
        user_emails = UserEmail.objects.filter(
            email__iexact=email, is_confirmed=True
        )
        num_results = user_emails.count()
        if num_results == 1:
            user = user_emails[0].user
        elif num_results > 1:
            # there should only be one User with this email...
            # if there are more, we have a data error!
            raise NonUniqueEmail(email)
        else:
            # num_results == 0, so check UserModel for active users with email
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(
                    email__iexact=email, is_active=True
                )
            except UserModel.MultipleObjectsReturned:
                user = None
                request = get_current_request()  # noqa: F841
                rollbar.report_exc_info()
                raise NonUniqueEmail(email)
            except UserModel.DoesNotExist:
                # also check newly registered accounts
                # if not user.is_active, handling will get passed downstream
                user = get_incomplete_signup_user_by_email(email)
    else:
        user = None
    return user


def get_user_by_email_with_retries(email, max_attempts=4):
    """Gets a User by `email`
    Wrapper for `get_user_by_email()` that will retry up to `max_attempts`.
    Used for mitigating possible race conditions during account creation.

    Returns None if not found
    """
    user = None
    attempt = 0
    while user is None and attempt < max_attempts:
        user = get_user_by_email(email)
        if user is None:
            time.sleep(2**attempt)
        attempt += 1
    return user


def get_incomplete_signup_user_by_email(email):
    """Gets an incomplete signup User by `email`
    Returns None if not found

    User MUST NOT be active
    """
    from htk.apps.accounts.models import UserEmail

    UserModel = get_user_model()
    user_emails = UserEmail.objects.filter(
        email__iexact=email,
        is_confirmed=False,
        user__is_active=False,
    )

    user = None
    user_email = user_emails.first()
    num_results = user_emails.count()

    if user_email is not None and num_results == 1:
        user = user_email.user
    elif num_results > 1:
        # there should only be one User with this email...
        # if there are more, we have a data error!
        raise NonUniqueEmail(email)
    else:
        try:
            user = UserModel.objects.get(email__iexact=email, is_active=False)
        except UserModel.DoesNotExist:
            user = None
    return user


##
# authentication


def authenticate_user(request, username, password):
    auth_user = authenticate(
        request=request, username=username, password=password
    )
    return auth_user


def authenticate_user_by_email(request, email, password):
    existing_user = get_user_by_email(email)
    if existing_user is not None:
        username = existing_user.username
        auth_user = authenticate_user(request, username, password)
    else:
        auth_user = None
    return auth_user


def authenticate_user_by_username_email(request, username_email, password):
    if is_valid_email(username_email):
        email = username_email
        auth_user = authenticate_user_by_email(request, email, password)
    else:
        username = username_email
        auth_user = authenticate_user(request, username, password)
    return auth_user


def authenticate_user_by_basic_auth_credentials(request, credentials):
    auth_user = None

    try:
        decoded_credentials = base64.b64decode(credentials).decode()
        credentials_parts = decoded_credentials.split(':', 1)
        if len(credentials_parts) == 2:
            username_email, password = credentials_parts
            auth_user = authenticate_user_by_username_email(
                request, username_email, password
            )
        else:
            pass

    except Exception:
        pass

    return auth_user


##
# email management


def get_user_email(user, email, is_confirmed=True):
    from htk.apps.accounts.models import UserEmail

    try:
        user_email = UserEmail.objects.get(
            user=user, email__iexact=email, is_confirmed=is_confirmed
        )
    except UserEmail.DoesNotExist:
        user_email = None
    return user_email


def associate_user_email(  # noqa: C901
    user,
    email,
    replacing=None,
    domain=None,
    email_template=None,
    email_subject=None,
    email_sender=None,
    confirmed=False,
):
    """Associates `email` with `user`

    Resulting UserEmail.is_confirmed = `confirmed`, default False

    Side effect: sends an activation email if `confirmed` == False

    Requires:
    `user` and `email` to be valid
    `email` cannot be confirmed by any other user
    `email` cannot already be associated with THIS `user`

    If `replacing` is specified, it denotes that it is being replaced by `email`
    """
    from htk.apps.accounts.models import UserEmail

    user_email = None
    if user and email:
        existing_user = get_user_by_email(email)
        should_associate = False
        if existing_user is None:
            # email address must not be associated to another account
            should_associate = True
        elif user == existing_user:
            if user.is_active:
                # an existing active account
                should_associate = True
            else:
                # a new registration
                should_associate = True
        else:
            # skip association
            # This email address is either:
            # a) already confirmed on another account
            # b) not already confirmed, and not a new registration
            should_associate = False

        if should_associate:
            user_email = get_user_email(user, email)
            if user_email is None:
                user_email = UserEmail.objects.create(
                    user=user,
                    email=email,
                    is_confirmed=confirmed,
                    replacing=replacing,
                )

            if confirmed or user_email.is_confirmed:
                # don't need to send activation email for a pre-confirmed address
                # pre-confirmed email can come from a social auth provider
                user_email.confirm_and_activate_account()
                if replacing:
                    from htk.apps.accounts.utils.notifiers import (
                        notify_user_email_update,
                    )

                    notify_user_email_update(user, replacing, email)

            elif not user_email.is_confirmed:
                domain = domain or htk_setting(
                    'HTK_DEFAULT_EMAIL_SENDING_DOMAIN'
                )
                try:
                    user_email.send_activation_email(
                        domain,
                        template=email_template,
                        subject=email_subject,
                        sender=email_sender,
                    )
                except Exception:
                    request = get_current_request()  # noqa: F841
                    rollbar.report_exc_info()
            else:
                pass
        else:
            pass
    else:
        # invalid user or email
        pass

    return user_email


def extract_user_email(username_email):
    """Gets the user for `username_email`
    `username_email` is a string that could be either a username OR an email
    """
    email = None
    if is_valid_email(username_email):
        email = username_email
        user = get_user_by_email(email)
    else:
        username = username_email
        user = get_user_by_username(username)

    return (
        user,
        email,
    )


def get_user_by_id(user_id):
    """Gets a User by user id"""
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(id=user_id)
    except UserModel.DoesNotExist:
        user = None
    return user


def get_users_by_id(user_ids, strict=False, preserve_ordering=False):
    """Gets a list of Users by user ids
    If `strict`, all user_ids must exist, or None is returned
    For non `strict`, returns a partial list of Users with matching ids
    """
    UserModel = get_user_model()
    from htk.utils.query import get_objects_by_id

    users = get_objects_by_id(
        UserModel, user_ids, strict=strict, preserve_ordering=preserve_ordering
    )
    return users


def get_user_emails_by_id(user_email_ids, strict=False):
    """Gets a list of UserEmails by ids
    If `strict`, all user_email_ids must exist, or None is returned
    For non `strict`, returns a partial list of UserEmails with valid ids
    """
    from htk.apps.accounts.models import UserEmail

    if strict:
        try:
            user_emails = [
                UserEmail.objects.get(id=user_email_id)
                for user_email_id in user_email_ids
            ]
        except UserEmail.DoesNotExist:
            user_emails = None
    else:
        user_emails = []
        for user_email_id in user_email_ids:
            try:
                user_email = UserEmail.objects.get(id=user_email_id)
                user_emails.append(user_email)
            except UserEmail.DoesNotExist:
                pass
    return user_emails


##
# user id manipulation


def encrypt_uid(user):
    """Encrypts the User id for transfer in plaintext

    Security through obscurity / Swiss cheese model
    """
    uid_xor = htk_setting('HTK_USER_ID_XOR')
    crypt_uid = int_to_base36(user.id ^ uid_xor)
    return crypt_uid


def decrypt_uid(encrypted_uid):
    uid_xor = htk_setting('HTK_USER_ID_XOR')
    user_id = base36_to_int(encrypted_uid) ^ uid_xor
    return user_id


def resolve_encrypted_uid(encrypted_uid):
    """Returns the User for this `encrypted_uid`

    Security through obscurity / Swiss cheese model
    """
    UserModel = get_user_model()
    try:
        user_id = decrypt_uid(encrypted_uid)
        user = UserModel.objects.get(id=user_id)
    except ValueError:
        user = None
    except UserModel.DoesNotExist:
        user = None
    return user


def parse_authorization_header(
    request: HttpRequest,
) -> tuple[T.Optional[str], T.Optional[str]]:
    """Parse the authorization header from the request

    Expected format: `<token_type> <token>`

    Examples:
    - `Authorization: Bearer <token>`
    - `Authorization: Basic <credentials>`

    Returns:
    - `token_type`: The type of token, e.g. `Bearer` or `Basic`
    - `token`: The token
    """
    token = None
    token_type = None

    if 'HTTP_AUTHORIZATION' in request.META:
        auth_header = request.META['HTTP_AUTHORIZATION']
        parts = auth_header.split()
        if len(parts) == 2:
            token_type, token = parts
        else:
            pass
    else:
        pass

    return token_type, token
