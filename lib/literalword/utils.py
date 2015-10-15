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
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        container = soup.select('.bMeatWrapper')[0]
        # remove <p> tags
        for p in container.find_all('p'):
            p.decompose()
        html = u'%s' % container
        text = html2markdown(html)
    else:
        text = 'Could not find passage. Please review your query or try again later.'
    passage = {
        'url' : response.url,
        'text' : text,
    }
    return passage
