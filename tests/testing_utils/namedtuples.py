from datetime import time
from typing import NamedTuple


class StartEndTimePair(NamedTuple):
    """A namedtuple with start time and end time pair."""

    start_time: time
    end_time: time
