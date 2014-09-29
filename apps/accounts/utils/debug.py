from django.contrib.auth import get_user_model

def get_duplicate_emails():
    """Sanity check to make sure no users in database have the same email address
    """
    UserModel = get_user_model()
    users = UserModel.objects.all()
    emails_seen = {}
    duplicate_emails = []
    for user in users:
        email = user.email.lower()
        if email in emails_seen:
            duplicate_emails.append(email)
        else:
            emails_seen[email] = True
    return duplicate_emails
