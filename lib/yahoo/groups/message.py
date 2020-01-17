# Python Standard Library Imports

# Third Party (PyPI) Imports
from bs4 import BeautifulSoup

# HTK Imports
from htk.utils.cache_descriptors import CachedAttribute


class YahooGroupsMessage(object):
    """Represents a Yahoo Groups message
    """
    def __init__(self, html):
        self.html = html

        soup = BeautifulSoup(html, 'html.parser')
        self.soup = soup

    @CachedAttribute
    def message(self):
        """Returns the main message text
        """
        main_div = self.soup.find(id='ygrp-text')
        paragraphs = main_div.find_all('p')
        for p in paragraphs:
            p.insert_after('<br/><br/>')

        message = main_div.text
        return message
