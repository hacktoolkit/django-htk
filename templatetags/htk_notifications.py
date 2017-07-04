from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('htk/fragments/notifications/dismissible_alert.html', takes_context=True)
def show_dismissible_alert(context, alert_name, alert_level, alert_template, user, *args, **kwargs):
    from htk.apps.notifications.utils import should_display_dismissible_alert
    context.update({
        'should_display_dismissible_alert' : should_display_dismissible_alert(alert_name, alert_template, user, context, *args, **kwargs),
        'alert_name' : alert_name,
        'alert_level' : alert_level,
        'alert_template' : alert_template,
    })
    return context
