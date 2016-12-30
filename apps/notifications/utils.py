from htk.utils import htk_setting
from htk.utils.general import resolve_method_dynamically

def get_user_dismissed_alert_attribute_key(alert_key):
    key = 'dismissed_alert:%s' % alert_key
    return key

def dismiss_alert(user, alert_key):
    attribute_key = get_user_dismissed_alert_attribute_key(alert_key)
    user.profile.set_attribute(attribute_key, True, as_bool=True)

def has_user_dismissed_alert(user, alert_key):
    attribute_key = get_user_dismissed_alert_attribute_key(alert_key)
    result = user.profile.get_attribute(attribute_key, as_bool=True)
    return result

def should_display_dismissible_alert(alert_name, alert_template, user, context, *args, **kwargs):
    result = False
    display_predicates = htk_setting('HTK_NOTIFICATIONS_DISMISSIBLE_ALERT_DISPLAY_PREDICATES')
    display_predicate_method = display_predicates.get(alert_name, None)
    if display_predicate_method:
        display_predicate = resolve_method_dynamically(display_predicate_method)
        result = display_predicate(alert_name, alert_template, user, context, *args, **kwargs)
    return result
