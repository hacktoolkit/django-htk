# Redfin Integration

Real estate property valuation and market data.

## Quick Start

```python
from htk.lib.redfin.api import get_avm, get_property_listing_id, get_home_worth_url

# Get property valuation (Automated Valuation Model)
avm = get_avm(property_id='12345')

# Get property listing ID
listing_id = get_property_listing_id(address)

# Get home worth URL
url = get_home_worth_url(property_id, listing_id)
```

## Configuration

```python
# settings.py
REDFIN_API_KEY = os.environ.get('REDFIN_API_KEY')
```

## Related Modules

- `htk.lib.zillow` - Real estate data
