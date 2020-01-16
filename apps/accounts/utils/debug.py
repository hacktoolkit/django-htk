# Django Imports
from django.contrib.auth import get_user_model


def get_duplicate_emails():
    """Sanity check to make sure no users in database have the same email address
    """
    UserModel = get_user_model()
    users = UserModel.objects.all()
    emails_seen = {}
    duplicate_emails = {}
    for user in users:
        email = user.email.strip().lower()
        if email:
            if email not in emails_seen:
                emails_seen[email] = True
            else:
                if email not in duplicate_emails:
                    duplicate_emails[email] = 1
                else:
                    duplicate_emails[email] += 1

    return sorted(duplicate_emails.keys())
