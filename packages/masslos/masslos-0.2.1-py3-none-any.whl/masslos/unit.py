import logging


class Unit:
    NDIGIT = 2

    def __init__(self, unit_dict):
        self.unit_dict = unit_dict

    def convert(self, value, from_unit, to_unit, ndigits=NDIGIT):
        """
        Converts a unit from from_unit to to_unit.

        Returns a float rounded to ndigits (default=2)
        """
        try:
            return float(
                self.unit_dict["".join(from_unit.lower().split())]
                * float(value)
                / self.unit_dict["".join(to_unit.lower().split())],
            ).__round__(ndigits)
        except KeyError:
            logger.warning(
                "function call with unknown unit(s): %s, %s",
                from_unit,
                to_unit,
            )
            return None
        except ValueError:
            logger.warning("function call with non decimal value: %s", value)
            return None

    def list_units(self):
        """Returns list of valide units."""
        return list(self.unit_dict.keys())


# Setting up Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("unit.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
