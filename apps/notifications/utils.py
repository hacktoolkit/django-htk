from htk.utils import htk_setting
from htk.utils.cache_descriptors import memoized
from htk.utils.general import resolve_method_dynamically

@memoized
def get_alert_key(alert_name):
    alert_key = None
    alert_key_generators = htk_setting('HTK_NOTIFICATIONS_DISMISSIBLE_ALERT_KEY_GENERATORS')
    generator_method = alert_key_generators.get(alert_name, None)
    if generator_method:
        generator = resolve_method_dynamically(generator_method)
        if generator:
            alert_key = generator(alert_name)
    return alert_key

def get_user_dismissed_alert_attribute_key(alert_key):
    key = 'dismissed_alert:%s' % alert_key
    return key

def dismiss_alert_for_user(user, alert_name):
    success = False
    alert_key = get_alert_key(alert_name)
    if alert_key:
        attribute_key = get_user_dismissed_alert_attribute_key(alert_key)
        user.profile.set_attribute(attribute_key, True, as_bool=True)
        success = True
    return success

def has_user_dismissed_alert(user, alert_name):
    alert_key = get_alert_key(alert_name)
    attribute_key = get_user_dismissed_alert_attribute_key(alert_key)
    result = user.profile.get_attribute(attribute_key, as_bool=True)
    return result

def should_display_dismissible_alert(alert_name, alert_template, user, context, *args, **kwargs):
    result = False
    display_predicates = htk_setting('HTK_NOTIFICATIONS_DISMISSIBLE_ALERT_DISPLAY_PREDICATES')
    display_predicate_method = display_predicates.get(alert_name, None)
    if display_predicate_method:
        display_predicate = resolve_method_dynamically(display_predicate_method)
        if display_predicate:
            result = display_predicate(alert_name, alert_template, user, context, *args, **kwargs)
    return result
