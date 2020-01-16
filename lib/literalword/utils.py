# Python Standard Library Imports
import re

# Third Party / PIP Imports
import requests
from bs4 import BeautifulSoup

# HTK Imports
from htk.lib.literalword.constants import *
from htk.utils.text.converters import html2markdown


def is_bible_version(version):
    _is_bible_version = version in LITERAL_WORD_URLS
    return _is_bible_version

def get_bible_version(version):
    version = version or DEFAULT_BIBLE_VERSION
    if not is_bible_version(version):
        version = DEFAULT_BIBLE_VERSION
    return version

def get_bible_passage(query, version=None):
    version = get_bible_version(version)
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
            # have to extract text using BeautifulSoup since Markdown syntax allows span tags, apparently
            html = '%s' % container.text
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
