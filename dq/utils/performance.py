import time
from contextlib import contextmanager
from datetime import datetime
from typing import Optional


class PerformanceCounter:
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: int = 0

    @contextmanager
    def timer(self):
        self.start_time = datetime.now()
        self.start_perf_counter = time.perf_counter()
        try:
            yield
        finally:
            self.end_time = datetime.now()
            self.end_perf_counter = time.perf_counter()
            self.duration = int((self.end_perf_counter - self.start_perf_counter) * 1000)  # Convert to milliseconds
