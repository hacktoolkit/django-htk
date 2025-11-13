# OhMyGreen API Constants

API endpoints and resources for OhMyGreen catering service integration.

## Constants

```python
from htk.lib.ohmygreen.constants import OHMYGREEN_API_BASE_URL, OHMYGREEN_API_RESOURCES
```

## API Base URL

```python
OHMYGREEN_API_BASE_URL = 'https://www.ohmygreen.com/api'
```

## API Resources

Dictionary mapping resource types to endpoint URLs:

```python
OHMYGREEN_API_RESOURCES = {
    'menu': 'https://www.ohmygreen.com/api/catering/menus',
}
```

## Usage Example

```python
from htk.lib.ohmygreen.constants import OHMYGREEN_API_RESOURCES

# Fetch menu data
menu_url = OHMYGREEN_API_RESOURCES['menu']
response = requests.get(menu_url)
```
