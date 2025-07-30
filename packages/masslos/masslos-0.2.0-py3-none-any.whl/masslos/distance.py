"""
Functions to convert distances.

The module supports
    - metric
    - imperial
    - astronomical
    - nautical
"""

import logging

from masslos import __DEFAULT_NDIGITS as DND

__unit_dict = {
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
}


def convert_distance(value, from_unit, to_unit, ndigits=DND):
    """
    Converts a distance from a one unit to another unit.

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


# imperial
def in_inch(value, unit, ndigits=DND):
    return convert_distance(value, unit, "in", ndigits)


def in_feet(value, unit, ndigits=DND):
    return convert_distance(value, unit, "ft", ndigits)


def in_yard(value, unit, ndigits=DND):
    return convert_distance(value, unit, "yd", ndigits)


def in_mile(value, unit, ndigits=DND):
    return convert_distance(value, unit, "mi", ndigits)


# metric
def in_meter(value, unit, ndigits=DND):
    return convert_distance(value, unit, "m", ndigits)


def in_cm(value, unit, ndigits=DND):
    return convert_distance(value, unit, "cm", ndigits)


def in_mm(value, unit, ndigits=DND):
    return convert_distance(value, unit, "mm", ndigits)


# Setting up Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("distance.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
