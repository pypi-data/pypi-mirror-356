"""
Functions to convert speeds.

The module supports
    - metric
    - imperial
    - astronomical
    - nautical
"""

from .unit import Unit


class Speed(Unit):
    def __init__(self):
        super().__init__(
            {
                "m/s": 1,
                "km/h": 0.2777778,
                "mph": 0.44704,
                "fps": 0.3048,
                "knot": 0.5144444,
                "mach": 343,
                "c": 299792458,
            },
        )

    def in_ms(self, value, from_unit, ndigits=Unit.NDIGIT):
        return self.convert(value, from_unit, "m/s", ndigits)

    def in_kmh(self, value, from_unit, ndigits=Unit.NDIGIT):
        return self.convert(value, from_unit, "km/h", ndigits)

    def in_mph(self, value, from_unit, ndigits=Unit.NDIGIT):
        return self.convert(value, from_unit, "mph", ndigits)

    def in_fps(self, value, from_unit, ndigits=Unit.NDIGIT):
        return self.convert(value, from_unit, "fps", ndigits)

    def in_knot(self, value, from_unit, ndigits=Unit.NDIGIT):
        return self.convert(value, from_unit, "knot", ndigits)

    def in_mach(self, value, from_unit, ndigits=Unit.NDIGIT):
        return self.convert(value, from_unit, "mach", ndigits)

    def in_c(self, value, from_unit, ndigits=Unit.NDIGIT):
        return self.convert(value, from_unit, "c", ndigits)
