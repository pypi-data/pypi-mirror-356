# Maßlos unit conversion library

## Usage:

```python
from masslos import convert_distance, convert_weight

# without specifying the decimal digits (default = 2)
dist_in_meter = convert_distance(10, "yd", "m")
weight_in_kg = convert_weight(11, "lbs", "kg")

# with specifying the decimal digits
dist_in_meter = convert_distance(value=10, from_unit="yd", to_unit="m", ndigits=3)
weight_in_kg = convert_weight(value=11, from_unit="lbs", to_unit="kg", ndigits=3)
```
