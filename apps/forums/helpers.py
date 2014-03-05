from django.core.urlresolvers import reverse

def wrap_data_forum(request, data=None):
    if data is None:
        data = {}
    data['forum_mode'] = True

    return data
