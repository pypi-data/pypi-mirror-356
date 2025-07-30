from importlib.metadata import version

from ._time_class import EpochTimestamp
from ._timer import TimerData, create_timer, timer
from ._tools import add_ord_suffix
from .constants.date_related import DATE_FORMAT, DATE_TIME_FORMAT
from .time_manager import TimeTools

__version__: str = version("bear-epoch-time")

__all__ = [
    "EpochTimestamp",
    "TimerData",
    "create_timer",
    "timer",
    "TimeTools",
    "add_ord_suffix",
    "DATE_FORMAT",
    "DATE_TIME_FORMAT",
    "__version__",
]
