# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.contrib import messages
from django.shortcuts import redirect

# HTK Imports
from htk.admintools.cachekeys import (
    HtkCompanyEmployeesCache,
    HtkCompanyOfficersCache,
)
from htk.apps.accounts.utils import (
    get_user_by_email,
    get_user_by_id,
    get_user_by_username,
)
from htk.utils import htk_setting
from htk.utils.request import get_current_request


def get_company_officers_id_email_map():
    """Gets a mapping of company officers

    Returns a dictionary mapping User ids to emails
    """
    c = HtkCompanyOfficersCache()
    officers_map = c.get()
    if officers_map is None:
        officers_map = {}
        for email in htk_setting('HTK_COMPANY_OFFICER_EMAILS'):
            user = get_user_by_email(email)
            if user:
                officers_map[user.id] = email
        c.cache_store(officers_map)
    return officers_map


def get_company_employees_id_email_map():
    """Gets a mapping of company employees

    Returns a dictionary mapping User ids to emails
    """
    c = HtkCompanyEmployeesCache()
    employees_map = c.get()
    if employees_map is None:
        employees_map = {}
        for email in htk_setting('HTK_COMPANY_EMPLOYEE_EMAILS'):
            user = get_user_by_email(email)
            if user:
                employees_map[user.id] = email
        c.cache_store(employees_map)
    return employees_map


def is_allowed_to_emulate_users(user):
    """Determines whether `user` is allowed to emulate other users"""
    allowed = False
    if user is not None and user.is_authenticated:
        try:
            user_profile = user.profile
            if user_profile.is_company_officer:
                allowed = True
        except:
            request = get_current_request()
            rollbar.report_exc_info(request=request)
    return allowed


def is_allowed_to_emulate(original_user, targeted_user):
    """Determines whether `original_user` is allowed to emulate `targeted_user`

    Emulating a company officer is disallowed.
    """
    allowed = (
        original_user
        and is_allowed_to_emulate_users(original_user)
        and targeted_user
        and not targeted_user.profile.is_company_officer
    )
    return allowed


def request_emulate_user(request, user_id=None, username=None):
    """If all conditions are met, will modify the request to set an emulated user"""
    is_attempting_to_emulate = user_id or username

    if is_attempting_to_emulate and is_allowed_to_emulate_users(request.user):
        if user_id:
            targeted_user = get_user_by_id(user_id)
        elif username:
            targeted_user = get_user_by_username(username)
        else:
            rollbar.report_message(
                'Impossible case: attempting to emulate another user, but none specified'
            )

        if targeted_user is None:
            messages.error(
                request,
                'Cannot Emulate: User does not exist',
                fail_silently=True,
            )
        else:
            if is_allowed_to_emulate(request.user, targeted_user):
                request.original_user = request.user
                request.user = targeted_user
            else:
                messages.error(
                    request,
                    'Cannot Emulate: Not allowed to emulate that user',
                    fail_silently=True,
                )
    else:
        # is not attempting to emulate users or is not allowed to emulate
        pass


def emulate_user(request, user_id=None, username=None, redirect_url='/'):
    request_emulate_user(request, user_id=user_id, username=username)
    response = redirect(redirect_url)

    cookie_name = (
        'emulate_user_id'
        if user_id
        else 'emulate_user_username'
        if username
        else None
    )

    cookie_value = user_id or username
    cookie_max_age = 60 * 60  # 1 hour in seconds

    response.set_cookie(cookie_name, value=cookie_value, max_age=cookie_max_age)

    return response
