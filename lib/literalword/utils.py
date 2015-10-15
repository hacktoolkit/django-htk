from bs4 import BeautifulSoup
import re
import requests

from htk.utils.text.converters import html2markdown

def get_bible_passage(query):
    BASE_URL = 'http://nasb.literalword.com/'
    url = BASE_URL
    params = {
        'q' : query,
    }
    response = requests.get(url, params)
    default_text = 'Could not find passage in Bible. Please review your query or try again later.'
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text_container = soup.select('.bMeatWrapper')
        if len(text_container):
            container = text_container
            # remove <p> tags
            for p in container.find_all('p'):
                p.decompose()
            html = u'%s' % container
            text = html2markdown(html)
        else:
            text = default_text
    else:
        text = default_text

    passage = {
        'url' : response.url,
        'text' : text,
    }
    return passage
