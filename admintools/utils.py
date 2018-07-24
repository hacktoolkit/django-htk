import rollbar

from htk.admintools.cachekeys import HtkCompanyEmployeesCache
from htk.admintools.cachekeys import HtkCompanyOfficersCache
from htk.apps.accounts.utils import get_user_by_email
from htk.utils import htk_setting

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

def can_emulate_another_user(user):
    can_emulate = False
    if user.is_authenticated():
        try:
            user_profile = user.profile
            if user_profile.is_company_officer:
                can_emulate = True
        except:
            rollbar.report_exc_info(request=request)
    return can_emulate
