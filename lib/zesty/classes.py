import copy
import datetime
import requests

from htk.lib.zesty.constants import *

class ZestyAPI(object):
    def __init__(self, zesty_id):
        self.zesty_id = zesty_id

    def get_url(self, resource_type, **kwargs):
        """Returns the resource URL for `resource_type`
        """
        url_values = {
            'zesty_id' : self.zesty_id,
        }
        url_values.update(kwargs)
        url = ZESTY_URLS.get(resource_type) % url_values
        return url

    def get_meals(self):
        """Retrieves meals from Zesty API
        """
        url = self.get_url('meals')
        response = requests.get(url)
        meals = None
        if response.status_code == 200:
            try:
                meals_data = response.json()
                meals = ZestyMeals(self, meals_data)
            except:
                pass
        else:
            pass
        return meals

    def get_dish(self, dish_id):
        """Retrieves a dish from Zesty API by `dish_id`
        """
        dish = None
        kwargs = {
            'dish_id' : dish_id,
        }
        url = self.get_url('dish', **kwargs)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                dish_data = response.json()
                dish = ZestyDish(self, dish_data)
            except:
                pass
        else:
            pass
        return dish

class ZestyMeals(object):
    DATE_STRING_FMT = '%Y-%m-%d'
    def __init__(self, api, data):
        """Parse meals data into an internal data structure
        """
        self.api = api
        # raw meals data as provided by Zesty API JSON response
        self.data = data

        # store as more useful data structure
        # meal_items keyed by id
        self.meal_items = { meal_item['id'] : meal_item for meal_item in data['meal_items'] }
        # meals keyed by YYYY-mm-dd
        self.meals = { meal['delivery_date'][:10] : meal for meal in data['meals'] }

    def get_meal_for_date(self, dt):
        date_str = dt.strftime(self.DATE_STRING_FMT)
        meal = self.meals.get(date_str)
        return meal

    def get_pretty_menu(self, dt, slack_attachments=False):
        """Returns a pretty Slack-compatible string representing menu for a meal on `dt`

        If `slack_attachments` is:
          - False, return only a plain Slack message
          - True, return rich Slack attachments
        """
        meal = None
        attempts = 0
        target_dt = dt
        # look up the first available meal within the next week
        while meal is None and attempts < 7:
            target_dt = dt + datetime.timedelta(days=attempts)
            meal = self.get_meal_for_date(target_dt)
            attempts += 1

        attachments = []
        # no meal was found
        if not meal:
            menu_str = 'There are no Zesty meals scheduled for the week of %s' % dt.strftime(self.DATE_STRING_FMT)
        else:
            menu_str = ''
            if attempts > 1:
                menu_str = 'There is no Zesty meal scheduled for %s, but the next meal is on %s.' % (
                    dt.strftime(self.DATE_STRING_FMT),
                    target_dt.strftime(self.DATE_STRING_FMT)
                )
                menu_str += '\n\n'
            meal_payload = self.get_pretty_menu_for_meal(meal, slack_attachments=slack_attachments)
            menu_str += meal_payload['text']
            attachments = meal_payload['attachments']
        payload = {
            'text' : menu_str,
            'attachments' : attachments,
        }
        return payload

    def get_pretty_dishes(self, meal, slack_attachments=False):
        meal_items = [self.meal_items[meal_item_id] for meal_item_id in meal['meal_item_ids']]
        pretty_dishes = []
        for meal_item in meal_items:
            dish_id = meal_item['dish_id']
            dish = self.api.get_dish(dish_id)
            if dish:
                if slack_attachments:
                    pretty_dish = dish.get_slack_attachment()
                else:
                    pretty_dish = dish.get_pretty()
            else:
                pretty_dish = '*%s*' % meal_item['name']
            pretty_dishes.append(pretty_dish)
        return pretty_dishes

    def _get_meal_dict(self, meal, slack_attachments=False):
        dt = datetime.datetime.strptime(meal['delivery_date'][:16], '%Y-%m-%dT%H:%M')
        meal_dict = copy.copy(meal)
        dishes = self.get_pretty_dishes(meal, slack_attachments=slack_attachments)
        meal_dict.update({
            'day_of_week' : dt.strftime('%A'),
            'meal_type' : meal['meal_type'].capitalize(),
            'time' : dt.strftime('%I:%M%p'),
            'date' : dt.strftime('%B %d, %Y'),
            'dishes' : dishes if slack_attachments else '\n\n'.join(dishes),
        })
        return meal_dict

    def get_pretty_menu_for_meal(self, meal, slack_attachments=False):
        meal_dict = self._get_meal_dict(meal, slack_attachments=slack_attachments)
        menu_str = """*%(day_of_week)s %(meal_type)s, %(time)s - %(date)s* at %(delivery_location_address)s""" % meal_dict
        attachments = []
        if slack_attachments:
            restaurant_attachment = {
                'title' : '%(restaurant_name)s (%(restaurant_cuisine)s)' % meal_dict,
                'text' : meal_dict['restaurant_description'],
                'image_url' : meal_dict['restaurant_full_image'],
            }
            attachments.append(restaurant_attachment)
            attachments += meal_dict['dishes']
        else:
            menu_str += """

*%(restaurant_name)s* (%(restaurant_cuisine)s)
%(restaurant_full_image)s
_%(restaurant_description)s_

%(dishes)s
""" % meal_dict
        meal_payload = {
            'text' : menu_str,
            'attachments' : attachments,
        }
        return meal_payload

class ZestyDish(object):
    def __init__(self, api, data):
        """Parse Zesty dish
        """
        self.api = api
        # raw dish data as provided by Zesty API JSON response
        self.data = data

    def _get_dict(self):
        dish = copy.copy(self.data['dish'])
        dish.update({
            'allergens' : ', '.join(dish['allergens']) or 'None',
        })
        return dish

    def get_pretty(self):
        dish = self._get_dict()
        formatted = """*%(name)s*
%(full_image_path)s
_%(description)s_

*Allergens*: %(allergens)s
*Total Calories*: %(calories)s
""" % dish
        return formatted

    def get_slack_attachment(self):
        dish = self._get_dict()
        attachment = {
            'title' : dish['name'],
            'text' : dish['description'],
            'image_url' : dish['full_image_path'],
        }
        return attachment
