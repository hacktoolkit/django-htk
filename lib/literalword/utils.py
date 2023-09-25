# Python Standard Library Imports
import re

# Third Party (PyPI) Imports
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
        'q': query,
    }
    response = requests.get(url, params)

    title = query

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text_container = soup.select('.bMeatWrapper')
        if len(text_container):
            container = text_container[0]

            title_container = container.select('.bTitle')
            if title_container:
                title = title_container[0].text.title()
            else:
                pass

            # add linebreaks for paragraphs
            paragraphs = container.select('.bPara')
            for paragraph in paragraphs:
                paragraph.replaceWith('<br/>')

            # add newlines for pericope headings
            pericopes = container.select('.bPeri')
            pericope_count = 0
            for pericope in pericopes:
                template = (
                    '<br/><br/><i>{}</i>' if pericope_count > 0 else '<i>{}</i>'
                )
                pericope.replaceWith(template.format(pericope.text))
                pericope_count += 1

            # remove <p> tags
            for p in container.find_all('p'):
                p.decompose()
            # have to extract text using BeautifulSoup since Markdown syntax allows span tags, apparently
            html = '%s' % container.text
            text = html2markdown(html)
        else:
            meta_description_tag = soup.meta.find(
                attrs={
                    'name': 'description',
                }
            )
            text = meta_description_tag['content']
    else:
        text = 'Could not find passage in Bible. Please review your query or try again later.'

    passage = {
        'url': response.url,
        'text': text,
    }
    return passage


def get_bible_passages(query, version=None):
    """Wrapper for get_bible_passage

    Returns a list of dicts representing Bible passages fetched from Literal Word
    """
    passages = [get_bible_passage(query, version=version)]
    result = {
        'url': passages[0]['url'],
        'passages': passages,
    }
    return result
