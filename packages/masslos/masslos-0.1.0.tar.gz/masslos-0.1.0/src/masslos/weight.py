"""
Functions to convert weights.

The module supports
    - metric
    - imperial
"""

import logging

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


def convert_weight(value, from_unit, to_unit):
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


# # imperial
def in_pound(value, unit):
    return convert_weight(value, unit, "lbs")


def in_ounce(value, unit):
    return convert_weight(value, unit, "oz")


# metric
def in_gram(value, unit):
    return convert_weight(value, unit, "g")


def in_kilogram(value, unit):
    return convert_weight(value, unit, "kg")


def in_tonne(value, unit):
    return convert_weight(value, unit, "t")


# Setting up Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("weight.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
