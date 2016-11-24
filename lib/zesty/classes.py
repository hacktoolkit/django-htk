import copy
import datetime
import requests
import rollbar

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
                extra_data = {
                    'zesty_id' : self.zesty_id,
                }
                rollbar.report_exc_info(extra_data=extra_data)
        else:
            pass
        return meals

    def get_meal(self, meal_id):
        """Retrieves one meal from Zesty API by `meal_id`
        """
        meal = None
        kwargs = {
            'meal_id' : meal_id,
        }
        url = self.get_url('meal', **kwargs)
        response = requests.get(url)
        if response.status_code == 200:
            try :
                meal_data = response.json()
                meal = ZestyMeal(self, meal_data)
            except:
                extra_data = {
                    'zesty_id' : self.zesty_id,
                    'meal_id' : meal_id,
                }
                rollbar.report_exc_info(extra_data=extra_data)
        else:
            pass
        return meal

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
                extra_data = {
                    'zesty_id' : self.zesty_id,
                    'dish_id' : dish_id,
                }
                rollbar.report_exc_info(extra_data=extra_data)
        else:
            pass
        return dish

class ZestyMeals(object):
    """Represents a collection of Zesty meals
    """
    DATE_STRING_FMT = '%Y-%m-%d'
    def __init__(self, api, data):
        """Parse meals data into an internal data structure
        """
        self.api = api
        # raw meals data as provided by Zesty API JSON response
        self.data = data

        # store as more useful data structure
        # meals keyed by YYYY-mm-dd
        self.meals = { meal['delivery_date'][:10] : meal for meal in data['meals'] }

    def get_meal_for_date(self, dt):
        date_str = dt.strftime(self.DATE_STRING_FMT)
        meal_data = self.meals.get(date_str)
        if meal_data:
            meal = self.api.get_meal(meal_data['id'])
            if meal is None:
                # use partial data as a backup if full meal data is not available
                meal = ZestyMeal(self.api, meal_data)
            else:
                pass
        else:
            meal = None
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
            meal_payload = meal.get_pretty_menu(slack_attachments=slack_attachments)
            menu_str += meal_payload['text']
            attachments = meal_payload['attachments']
        payload = {
            'text' : menu_str,
            'attachments' : attachments,
        }
        return payload

class ZestyMeal(object):
    """Represents one Zesty meal for a specific day
    """
    def __init__(self, api, data):
        """Parse meal data into an internal data structure
        """
        self.api = api
        # raw meal metadata as provided by Zesty API JSON response
        self.data = data

        if 'meals' in data:
            # from the meal API
            self.meal = data.get('meals')[0]
        else:
            # from the meal metadata from meals API
            self.meal = data

        # meal_items keyed by id
        self.meal_items = data.get('meal_items', [])

    def _get_meal_dict(self, slack_attachments=False):
        """Get menu render data dict
        """
        meal = self.meal
        dt = datetime.datetime.strptime(meal['delivery_date'][:16], '%Y-%m-%dT%H:%M')
        meal_dict = copy.copy(meal)
        dishes = self.get_pretty_dishes(slack_attachments=slack_attachments)
        meal_dict.update({
            'day_of_week' : dt.strftime('%A'),
            'meal_type' : meal['meal_type'].capitalize(),
            'time' : dt.strftime('%I:%M%p'),
            'date' : dt.strftime('%B %d, %Y'),
            'dishes' : dishes if slack_attachments else '\n\n'.join(dishes),
        })
        return meal_dict

    def get_pretty_menu(self, slack_attachments=False):
        meal_dict = self._get_meal_dict(slack_attachments=slack_attachments)
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

    def get_pretty_dishes(self, slack_attachments=False):
        """Makes API calls to fetch individual dish data
        """
        pretty_dishes = []
        for meal_item in self.meal_items:
            dish_id = meal_item['dish_id']
            dish = self.api.get_dish(dish_id)
            if dish and dish.is_valid:
                if slack_attachments:
                    pretty_dish = dish.get_slack_attachment()
                else:
                    pretty_dish = dish.get_pretty()
            else:
                pretty_dish = '*%s*' % meal_item['name']
            pretty_dishes.append(pretty_dish)
        return pretty_dishes

class ZestyDish(object):
    def __init__(self, api, data):
        """Parse Zesty dish
        """
        self.api = api
        # raw dish data as provided by Zesty API JSON response
        self.data = data
        self.is_valid = 'dishes' in self.data

    def _get_dict(self):
        dishes = self.data.get('dishes', [])
        dish = {}
        if dishes:
            dish = copy.copy(dishes[0])
            dish.update({
                'allergens' : ', '.join(dish.get('allergens', [])) or 'None',
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
