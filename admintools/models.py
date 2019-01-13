from htk.utils import htk_setting
from htk.utils.cache_descriptors import CachedAttribute

class HtkCompanyUserMixin(object):
    """Mixin for htk.apps.accounts.BaseAbstractUserProfile
    """

    @CachedAttribute
    def is_company_officer(self):
        """Determines whether this User is a company officer

        Officer list is in HTK_COMPANY_OFFICER_EMAILS
        (User.is_staff and User.is_superuser)=True is also considered a company officer
        """
        is_officer = False
        if self.user.is_staff and self.user.is_superuser:
            is_officer = True
        else:
            from htk.admintools.utils import get_company_officers_id_email_map
            officers_map = get_company_officers_id_email_map()
            officer_email = officers_map.get(self.user.id)
            if officer_email:
                is_officer = self.has_email(officer_email)
        return is_officer

    @CachedAttribute
    def is_company_employee(self):
        """Determines whether this User is a company employee

        Employee list is in htk.admintools.constants
        User.is_staff=True is also considered a company employee
        """
        is_employee = False
        if (self.user.is_staff and self.user.is_superuser) or self.is_company_officer:
            is_employee = True
        else:
            from htk.admintools.utils import get_company_employees_id_email_map
            employees_map = get_company_employees_id_email_map()
            employee_email = employees_map.get(self.user.id)
            if employee_email:
                is_employee = self.has_email(employee_email)
        return is_employee

    @CachedAttribute
    def has_company_email_domain(self):
        """Determines whether this User has email with company domain
        """
        company_email_domains = htk_setting('HTK_COMPANY_EMAIL_DOMAINS')
        company_email_domains_re = '|'.join([domain.replace(r'\.', r'\.') for domain in company_email_domains])
        value = bool(re.match(r'^[A-Za-z0-9\.\+_-]+@(%s)' % company_email_domains_re, self.user.email))
        return value

    def can_emulate_user(self):
        from htk.utils.request import get_current_request
        request = get_current_request()
        can_emulate = self.user.profile.is_company_employee or request.original_user.profile.is_company_employee
        return can_emulate
