import requests

from htk.lib.esv.constants import *

def esvapi_get_passage(passage, key='IP', archive=False):
    params = {
        'key' : key,
        'passage' : passage,
        'include-footnotes' : 0,
        'include-footnote-links' : 0,
        'include-copyright' : 0,
        'include-short-copyright' : 0,
        'include-passage-horizontal-lines' : 0,
        'include-heading-horizontal-lines' : 0,
        'include-passage-references' : 0,
        'include-verse-numbers' : 0,
    }
    if archive:
       params.update({
           'include-passage-references' : 1,
           'include-verse-numbers' : 1,
           'include-audio-link' : 1,
           'audio-format' : 'mp3',
           'audio-version' : 'mm',
       })
    response = requests.get(ESV_API_PASSAGE_QUERY_URL, params=params)
    html = response.content
    return html
