import random
from uuid import uuid4

from django.contrib.auth import get_user_model

from htk.test_scaffold.test_data import *

def create_test_user():
    """Creates a new user with random username for testing
    If two randomly assigned usernames overlap, it will fail
    """
    UserModel = get_user_model()
    username = '%s_%s' % ('test', uuid4().get_hex()[:10],)
    user = UserModel.objects.create(username=username)
    return user

def create_test_email():
    email = 'test%s@%s' % (
        uuid4().get_hex()[:10],
        'hacktoolkit.com',
    )
    return email

def create_test_username():
    """Generates a random username
    """
    username = '%s_%s' % ('test', uuid4().get_hex()[:10],)
    return username

def create_test_password():
    password = uuid4().get_hex()
    return password

def create_test_user_with_email_and_password():
    user = create_test_user()
    email = create_test_email()
    password = create_test_password()
    user.email = email
    user.set_password(password)
    user.save()
    return (user, email, password,)

def get_test_display_name():
    display_name = random.choice(TEST_DISPLAY_NAMES) + str(random.randint(1, 1000000))
    return display_name

def get_test_username():
    username = random.choice(TEST_USERNAMES) + str(random.randint(1, 1000000))
    return username

def get_random_string(max_length=0):
    s = 'randstr%s' % uuid4().get_hex()
    if max_length > 0:
        s = s[:max_length]
    return s
