from django.core.urlresolvers import reverse

from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically

def get_admin_urls():
    from htk.apps.cpq.constants.general import CPQ_APP_MODEL_NAMES
    admin_urls = []
    app_label = htk_setting('HTK_DEFAULT_APP_LABEL')
    for app_model_name in CPQ_APP_MODEL_NAMES:
        app_model = resolve_model_dynamically('%s.%s' % (app_label, app_model_name,))
        admin_url = {
            'url' : reverse('admin:%s_%s_changelist' % (app_label, app_model_name,)),
            'name' : app_model._meta.verbose_name_plural.title(),
        }
        admin_urls.append(admin_url)
    return admin_urls

def get_reporting_urls():
    from htk.apps.cpq.constants.general import CPQ_REPORTING_URL_NAMES
    reporting_urls = []
    for reporting_url_name in CPQ_REPORTING_URL_NAMES:
        reporting_url = {
            'url' : reverse('cpq_%s' % reporting_url_name),
            'name' : reporting_url_name.title(),
        }
        reporting_urls.append(reporting_url)
    return reporting_urls
