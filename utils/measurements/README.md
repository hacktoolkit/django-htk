# Measurements Utilities

Distance and weight unit conversions.

## Quick Start

```python
from htk.utils.measurements.distance import DistanceType
from htk.utils.measurements.weight import WeightType
from htk.utils.measurements.units import Distance, Weight

# Create distance measurements
distance = DistanceType(value=100, unit=Distance.METERS)
distance_in_miles = distance.to(Distance.MILES)

# Create weight measurements
weight = WeightType(value=150, unit=Weight.POUNDS)
weight_in_kg = weight.to(Weight.KILOGRAMS)
```

## Common Patterns

```python
# Convert between units
def convert_measurements(value, from_unit, to_unit):
    measurement = DistanceType(value, from_unit)
    return measurement.to(to_unit)

# Store canonical units in database, convert for display
distance_meters = DistanceType(1609.34, Distance.METERS)  # 1 mile
distance_miles = distance_meters.to(Distance.MILES)  # Display as 1 mile
```
