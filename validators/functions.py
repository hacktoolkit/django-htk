# Django Imports
from django.core.validators import validate_email


def is_valid_email(email):
    try:
        validate_email(email)
        is_valid = True
    except:
        is_valid = False
    return is_valid
