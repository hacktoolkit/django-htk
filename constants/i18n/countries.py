# Python Standard Library Imports
import json
import os


COUNTRIES_EN_JSON_FILE = os.path.realpath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'data',
        'countries',
        'country-en.json',
    )
)


with open(COUNTRIES_EN_JSON_FILE, 'r') as f:
    COUNTRIES_EN_NAMES_MAP = json.loads(f.read())
