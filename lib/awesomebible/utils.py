# Python Standard Library Imports
import urllib

# Third Party (PyPI) Imports
import requests


def get_bible_passage(query, version=None):
    url = 'https://awesome.bible/api/bible/passage'
    params = {
        'q': query,
        'v': version,
    }
    response = requests.get(url, params=params)

    title = query

    if response.status_code == 200:
        response_json = response.json()
        ref = response_json['ref']
        text = '\n'.join([verse['text'] for verse in response_json['verses']])
        q = urllib.parse.quote_plus(ref)
        passage = {
            'ref': ref,
            'url': f'https://awesome.bible/bible?q={q}',
            'text': text,
        }
    else:
        passage = None

    return passage
