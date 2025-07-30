"""
Functions to convert distances.

The module supports
    - metric
    - imperial
    - astronomical
    - nautical
"""

from .unit import Unit


class Distance(Unit):
    def __init__(self):
        super().__init__(
            {
                "meter": 1,
                "m": 1,
                "decimeter": 0.1,
                "dm": 0.1,
                "centimeter": 0.01,
                "cm": 0.01,
                "millimeter": 0.001,
                "mm": 0.001,
                "kilometer": 1000,
                "km": 1000,
                "inch": 0.0254,
                "in": 0.0254,
                "hand": 0.1016,
                "hh": 0.1016,
                "feet": 0.3048,
                "ft": 0.3048,
                "yard": 0.9144,
                "yd": 0.9144,
                "chain": 20.1168,
                "ch": 20.1168,
                "furlong": 201.168,
                "fur": 201.168,
                "mile": 1609.344,
                "mi": 1609.344,
                "league": 4828.032,
                "lea": 4828.032,
                "lightyear": 9.4607e15,
                "ly": 9.4607e15,
                "parsec": 3.0857e16,
                "pc": 3.0857e16,
                "astronomicalunit": 1.495979e11,
                "au": 1.495979e11,
                "nauticalmile": 0.0005399568,
                "nmi": 0.0005399568,
            },
        )

    # imperial
    def in_inch(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "in", ndigits)

    def in_feet(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "ft", ndigits)

    def in_yard(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "yd", ndigits)

    def in_mile(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "mi", ndigits)

    # metric
    def in_meter(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "m", ndigits)

    def in_cm(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "cm", ndigits)

    def in_mm(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "mm", ndigits)
