__DEFAULT_NDIGITS = 2  # when not specified, ndigits defaults to this value

from .distance import convert_distance  # noqa: E402, F401
from .weight import convert_weight  # noqa: E402, F401


def hello() -> str:
    return "Hello from masslos!"
