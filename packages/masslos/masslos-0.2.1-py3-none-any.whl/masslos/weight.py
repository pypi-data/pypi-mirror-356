"""
Functions to convert weights.

The module supports
    - metric
    - imperial
"""

from .unit import Unit


class Weight(Unit):
    def __init__(self):
        super().__init__(
            {
                "kilogram": 1,
                "kg": 1,
                "gram": 0.001,
                "g": 0.001,
                "tonne": 1000,
                "t": 1000,
                "metricton": 1000,
                "pound": 0.45359237,
                "lbs": 0.45359237,
                "ounce": 0.02834952,
                "oz": 0.02834952,
            },
        )

    # imperial
    def in_pound(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "lbs", ndigits)

    def in_ounce(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "oz", ndigits)

    # metric
    def in_gram(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "g", ndigits)

    def in_kilogram(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "kg", ndigits)

    def in_tonne(self, value, unit, ndigits=Unit.NDIGIT):
        return self.convert(value, unit, "t", ndigits)
