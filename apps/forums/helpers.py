from django.urls import reverse

def wrap_data_forum(request, data=None):
    if data is None:
        data = {}
    data['forum_mode'] = True

    return data
