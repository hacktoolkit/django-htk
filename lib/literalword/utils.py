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
        text_container = soup.select('.bMeatWrapper')
        if len(text_container):
            container = text_container
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
