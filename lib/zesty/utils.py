from htk.lib.zesty.classes import ZestyAPI

def get_zesty_lunch_menu(zesty_id, dt):
    """Get Zesty lunch menu for account `zesty_id` on `dt`
    """
    zesty_api = ZestyAPI(zesty_id)
    meals = zesty_api.get_meals()
    attachments = []

    if meals is None:
        menu_content = """Error retrieving today's lunch menu."""
    else:
        menu_payload = meals.get_pretty_menu(dt, slack_attachments=True)
        menu_content = menu_payload['text']
        attachments = menu_payload['attachments']

    values = {
        'web_meals_url' : zesty_api.get_url('web_meals_today'),
        'menu_content' : menu_content,
    }
    message = """%(menu_content)s

*View on web*: %(web_meals_url)s""" % values
    payload = {
        'text' : message,
        'attachments' : attachments,
    }
    return payload

def get_zesty_lunch_menu_ssml(zesty_id, dt):
    """Get Zesty lunch menu for account `zesty_id` on `dt` formatted as SSML
    """
    zesty_api = ZestyAPI(zesty_id)
    meals = zesty_api.get_meals()
    attachments = []

    if meals is None:
        ssml = """<speak>Error retrieving today's lunch menu.</speak>"""
    else:
        ssml = meals.get_menu_ssml(dt)
    return ssml

