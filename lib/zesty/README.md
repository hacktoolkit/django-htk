# Zesty

## Classes
- **`ZestyMeals`** (zesty/classes.py) - Represents a collection of Zesty meals
- **`ZestyMeal`** (zesty/classes.py) - Represents one Zesty meal for a specific day

## Functions
- **`get_url`** (zesty/classes.py) - Returns the resource URL for `resource_type`
- **`get_meal_today`** (zesty/classes.py) - Retrieves today's meal from Zesty API
- **`get_meals`** (zesty/classes.py) - Retrieves meals from Zesty API
- **`get_meal`** (zesty/classes.py) - Retrieves one meal from Zesty API by `meal_id`
- **`get_dish`** (zesty/classes.py) - Retrieves a dish from Zesty API by `dish_id`
- **`get_pretty_menu`** (zesty/classes.py) - Returns a pretty Slack-compatible string representing menu for a meal on `dt`
- **`get_menu_ssml`** (zesty/classes.py) - Returns an SSML string representing menu for a meal on `dt`
- **`get_pretty_dishes`** (zesty/classes.py) - Makes API calls to fetch individual dish data
- **`get_menu_ssml`** (zesty/classes.py) - Get menu for this meal as SSML (speech synthesis markup language)
- **`get_zesty_lunch_menu`** (zesty/utils.py) - Get Zesty lunch menu for account `zesty_id` on `dt`
- **`get_zesty_lunch_menu_ssml`** (zesty/utils.py) - Get Zesty lunch menu for account `zesty_id` on `dt` formatted as SSML
