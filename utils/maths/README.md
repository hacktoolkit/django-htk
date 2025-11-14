# Math Utilities

Mathematical functions for algebra and trigonometry.

## Quick Start

```python
from htk.utils.maths.algebra import quadratic
from htk.utils.maths.trigonometry import deg2rad, rad2deg

# Solve quadratic equation (ax² + bx + c = 0)
roots = quadratic(a=1, b=-3, c=2)  # Returns: (2.0, 1.0)

# Convert between degrees and radians
radians = deg2rad(180)  # 3.14159...
degrees = rad2deg(3.14159)  # 180.0
```

## Common Patterns

```python
# Find solutions to quadratic equations
a, b, c = coefficients()
solutions = quadratic(a, b, c)

# Work with angles
angle_degrees = 45
angle_radians = deg2rad(angle_degrees)
# Use in calculations...
angle_back = rad2deg(angle_radians)
```
