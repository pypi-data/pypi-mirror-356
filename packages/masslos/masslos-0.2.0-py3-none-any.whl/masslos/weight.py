"""
Functions to convert weights.

The module supports
    - metric
    - imperial
"""

import logging

from masslos import __DEFAULT_NDIGITS as DND

__unit_dict = {
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
}


def convert_weight(value, from_unit, to_unit, ndigits=DND):
    """
    Converts a weight from a one unit to another unit.

    Returns a float rounded to ndigits (default=2)
    """
    try:
        return float(
            __unit_dict["".join(from_unit.lower().split())]
            * float(value)
            / __unit_dict["".join(to_unit.lower().split())],
        ).__round__(ndigits)
    except KeyError:
        logger.warning("function call with unknown unit(s): %s, %s", from_unit, to_unit)
        return None
    except ValueError:
        logger.warning("function call with non decimal value: %s", value)
        return None


# # imperial
def in_pound(value, unit, ndigits=DND):
    return convert_weight(value, unit, "lbs", ndigits)


def in_ounce(value, unit, ndigits=DND):
    return convert_weight(value, unit, "oz", ndigits)


# metric
def in_gram(value, unit, ndigits=DND):
    return convert_weight(value, unit, "g", ndigits)


def in_kilogram(value, unit, ndigits=DND):
    return convert_weight(value, unit, "kg", ndigits)


def in_tonne(value, unit, ndigits=DND):
    return convert_weight(value, unit, "t", ndigits)


# Setting up Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("weight.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
