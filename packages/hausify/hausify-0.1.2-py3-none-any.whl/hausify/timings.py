import datetime as dt
from typing import Optional


class Timings:
    def __init__(self) -> None:
        self.start = dt.datetime.now()
        self.end: Optional[dt.datetime] = None

    def stop(self) -> None:
        self.end = dt.datetime.now()

    @property
    def duration_ms(self) -> int:
        if self.end is None:
            raise ValueError("Timings have not been stopped yet.")
        return round((self.end - self.start).total_seconds() * 1000)
