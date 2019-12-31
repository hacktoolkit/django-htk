# Python Standard Library Imports

# Third Party / PIP Imports
import requests
import rollbar

# Django Imports

# HTK Imports
from htk.lib.ohmygreen.constants import *

class OhMyGreenAPI(object):
    def __init__(self, company_id, company):
        self.company_id = company_id
        self.company = company

    def get_web_url(self):
        url = 'https://www.ohmygreen.com/%s/catering_menu' % (
            self.company,
        )
        return url

    def get_menu(self, dt):
        url = OHMYGREEN_API_RESOURCES['menu']
        data = {
            #'company' : self.company,
            'company_id' : self.company_id,
            'date' : dt.strftime('%m/%d/%Y'),
        }
        response = requests.post(url, data=data)
        menu_data = response.json().get('menu', {})
        menu = OhMyGreenMenu(self, menu_data)
        return menu

class OhMyGreenMenu(object):
    def __init__(self, api, menu_data):
        self.api = api
        self.data = menu_data

    def get_slack_message(self):
        def _build_meal_string(meal, meal_data):
            data = {
                'meal' : meal,
                'date' : meal_data['date'],
                'entrees' : ', '.join([dish['name'] for dish in meal_data.get('dishes', {}).get('ent', [])]),
                'veg_entrees' : ', '.join([dish['name'] for dish in meal_data.get('dishes', {}).get('veg', [])]),
                'sides' : ', '.join([dish['name'] for dish in meal_data.get('dishes', {}).get('sid', [])]),
                'desserts' : ', '.join([dish['name'] for dish in meal_data.get('dishes', {}).get('des', [])]) or 'None',
            }
            tpl = """*%(meal)s for %(date)s*
*Entrees*: %(entrees)s
*Vegetarian Entrees*: %(veg_entrees)s
*Sides*: %(sides)s
*Dessert*: %(desserts)s
"""
            return tpl % data

        meal_strings = []
        for meal, meal_data in self.data.items():
            meal_strings.append(_build_meal_string(meal, meal_data))

        if len(meal_strings):
            meals = '\n\n'.join(meal_strings)
        else:
            meals = 'There is no meal scheduled for today.'

        msg = '%s\n\n*View on web*: %s' % (
            meals,
            self.api.get_web_url(),
        )

        return msg
