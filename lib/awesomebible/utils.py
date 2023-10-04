# Python Standard Library Imports
import urllib

# Third Party (PyPI) Imports
import requests
from bs4 import BeautifulSoup


def get_bible_passages(query, version=None):
    url = 'https://awesome.bible/api/bible/passage'
    params = {
        'q': query,
        'v': version,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        q = urllib.parse.quote_plus(query)
        url = f'https://awesome.bible/bible?q={q}'

        response_json = response.json()
        passages = [
            {
                'ref': passage['ref'],
                'text': '\n'.join(
                    [
                        _format_html_to_plaintext(verse['html'])
                        for verse in passage['verses']
                    ]
                ),
            }
            for passage in response_json
        ]

        result = {
            'url': url,
            'passages': passages,
        }
    else:
        result = None

    return result


def _format_html_to_plaintext(html):
    soup = BeautifulSoup(html)
    plaintext = soup.text
    return plaintext
