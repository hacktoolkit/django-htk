import requests

from htk.lib.esv.constants import *

def esvapi_get_passage(passage, key='IP'):
    params = {
        'key' : key,
        'passage' : passage,
        'include-short-copyright' : 0,
        'include-passage-horizontal-lines' : 0,
        'include-heading-horizontal-lines' : 0,
    }
    response = requests.get(ESV_API_PASSAGE_QUERY_URL, params=params)
    html = response.content
    return html
