# Python Standard Library Imports
import random

# Django Imports
from django.contrib.auth import get_user_model

# HTK Imports
from htk.compat import uuid4_hex
from htk.test_scaffold.test_data import *
from htk.utils import htk_setting


def create_test_user(
    username=None,
    first_name='',
    last_name='',
    email='',
):
    """Creates a new user with random username for testing
    If two randomly assigned usernames overlap, it will fail
    """
    UserModel = get_user_model()

    if username is None:
        username = create_test_username()

    user = UserModel.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    return user


def create_test_email(email_domain=None):
    if email_domain is None:
        email_domain = htk_setting('HTK_TEST_EMAIL_DOMAIN')

    email = 'test+{}@{}'.format(
        uuid4_hex()[:10],
        email_domain,
    )
    return email


def create_test_username():
    """Generates a random username"""
    username = '{}_{}'.format(
        'test',
        uuid4_hex()[:10],
    )
    return username


def create_test_password():
    password = uuid4_hex()
    return password


def create_test_user_with_email_and_password():
    email = create_test_email()
    user = create_test_user(email=email)

    password = create_test_password()
    user.set_password(password)
    user.save()

    return (
        user,
        email,
        password,
    )


def get_test_display_name():
    display_name = random.choice(TEST_DISPLAY_NAMES) + str(
        random.randint(1, 1000000)
    )
    return display_name


def get_test_username():
    username = random.choice(TEST_USERNAMES) + str(random.randint(1, 1000000))
    return username


def get_random_string(max_length=0):
    s = 'randstr%s' % uuid4_hex()
    if max_length > 0:
        s = s[:max_length]
    return s
