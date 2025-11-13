# Zesty Integration

Meal planning and corporate catering service.

## Quick Start

```python
from htk.lib.zesty.classes import ZestyMeals, get_meal_today, get_pretty_menu

# Get today's meal
meal = get_meal_today(zesty_id)

# Get meals for date range
meals = get_meals(start_date, end_date)

# Get pretty menu for display
menu = get_pretty_menu(meal, date)

# Get menu as SSML (for voice assistants)
ssml = get_menu_ssml(meal, date)
```

## Configuration

```python
# settings.py
ZESTY_API_KEY = os.environ.get('ZESTY_API_KEY')
```

## Related Modules

- `htk.lib.ohmygreen` - Wellness benefits
- `htk.lib.alexa` - Voice integration
