# Django Imports
from django.conf import settings
from django.urls import reverse

# HTK Imports
from htk.mailers import send_email
from htk.utils import htk_setting
from htk.utils.urls import build_full_url


def send_invitation_email(request, invitation, early_access_code=None):
    """Sends invitation E-mail to given person"""
    invitation_response_url = reverse(
        htk_setting('HTK_ORGANIZATION_INVITATION_RESPONSE_URL_NAME'),
        kwargs={
            htk_setting(
                'HTK_ORGANIZATION_INVITATION_RESPONSE_URL_KWARG'
            ): invitation.organization.ulid
        },
    )
    query_string = (
        f'?early_access_code={early_access_code}' if early_access_code else ''
    )

    invitation_url = build_full_url(
        f'{invitation_response_url}{query_string}', request
    )

    context = {'invitation': invitation, 'invitation_url': invitation_url}
    send_email(
        sender=settings.HTK_DEFAULT_EMAIL_SENDER,
        to=[invitation.email],
        subject=htk_setting('HTK_ORGANIZATION_INVITATION_EMAIL_SUBJECT').format(
            invitation.organization.name
        ),
        template=htk_setting('HTK_ORGANIZATION_INVITATION_EMAIL_TEMPLATE_NAME'),
        context=context,
    )
