"""
Functions to convert distances.

The module supports
    - metric
    - imperial
    - astronomical
    - nautical
"""

import logging

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


def convert_distance(value, from_unit, to_unit):
    try:
        return (
            __unit_dict["".join(from_unit.lower().split())]
            * float(value)
            / __unit_dict["".join(to_unit.lower().split())]
        )
    except KeyError:
        logger.warning("function call with unknown unit(s): %s, %s", from_unit, to_unit)
        return None
    except ValueError:
        logger.warning("function call with non decimal value: %s", value)
        return None


# imperial
def in_inch(value, unit):
    return convert_distance(value, unit, "in")


def in_feet(value, unit):
    return convert_distance(value, unit, "ft")


def in_yard(value, unit):
    return convert_distance(value, unit, "yd")


def in_mile(value, unit):
    return convert_distance(value, unit, "mi")


# metric
def in_meter(value, unit):
    return convert_distance(value, unit, "m")


def in_cm(value, unit):
    return convert_distance(value, unit, "cm")


def in_mm(value, unit):
    return convert_distance(value, unit, "mm")


# Setting up Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("distance.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
