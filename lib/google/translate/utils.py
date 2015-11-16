import json
import requests
import urllib

from htk.lib.google.translate.constants import *

def get_language_code(language):
    language_code = None
    for code, lang in LANGUAGES.iteritems():
        if lang.lower() == language.lower():
            language_code = code
            break
    return language_code

def translate(term, origin='auto', target='en'):
    """Translates `term` from `origin` language into `target` language

    Inspired by: https://github.com/hubot-scripts/hubot-google-translate/blob/master/src/google-translate.coffee
    """
    url = GOOGLE_TRANSLATE_SINGLE_API_URL
    params = {
        'client' : 't',
        'hl' : 'en',
        'sl' : origin,
        'ssel' : 0,
        'tl' : target,
        'tsel' : 0,
        'q' : urllib.quote(term),
        'ie' : 'UTF-8',
        'oe' : 'UTF-8',
        'otf' : 1,
        'dt' : [
            'bd',
            'ex',
            'ld',
            'md',
            'qca',
            'rw',
            'rm',
            'ss',
            't',
            'at',
        ],
    }
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
    }
    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    translated = None
    if response.status_code == requests.codes.okay:
        try:
            if len(response.content) > 4 and response.content[0] == '[':
                parsed = response.json()
                #parsed = json.loads(response.content)
                language_code = parsed[2]
                language = LANGUAGES[language_code]
                translated = parsed[0] and parsed[0][0] and parsed[0][0][0]
            else:
                raise Exception('Invalid JSON')
        except e:
            return 'Failed to parse GAPI response'
    else:
        pass
    return translated
