# Zillow Integration

Real estate property valuation and Zestimate.

## Quick Start

```python
from htk.lib.zillow.utils import get_zestimate

# Get Zestimate for property
zestimate = get_zestimate(zpid='12345')
print(zestimate['value'], zestimate['last_updated'])
```

## Configuration

```python
# settings.py
ZILLOW_API_KEY = os.environ.get('ZILLOW_API_KEY')
```

## Related Modules

- `htk.lib.redfin` - Alternative property valuation
