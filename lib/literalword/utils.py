from bs4 import BeautifulSoup
import re
import requests

from htk.lib.literalword.constants import *
from htk.utils.text.converters import html2markdown

def get_bible_passage(query, version=None):
    version = version or DEFAULT_BIBLE_VERSION
    url = LITERAL_WORD_URLS.get(version, DEFAULT_BIBLE_VERSION)
    params = {
        'q' : query,
    }
    response = requests.get(url, params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text_container = soup.select('.bMeatWrapper')
        if len(text_container):
            container = text_container[0]
            # remove <p> tags
            for p in container.find_all('p'):
                p.decompose()
            html = u'%s' % container
            text = html2markdown(html)
        else:
            meta_description_tag = soup.meta.find(attrs={'name' : 'description',})
            text = meta_description_tag['content']
    else:
        text = 'Could not find passage in Bible. Please review your query or try again later.'

    passage = {
        'url' : response.url,
        'text' : text,
    }
    return passage
