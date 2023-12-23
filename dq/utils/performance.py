import time
from contextlib import contextmanager
from datetime import datetime


class PerformanceCounter:
    start_time: datetime = datetime.now()
    end_time: datetime = datetime.now()
    duration: float = 0

    @contextmanager
    def timer(self):
        self.start_time = datetime.now()
        self.start_perf_counter = time.perf_counter()
        try:
            yield
        finally:
            self.end_time = datetime.now()
            self.end_perf_counter = time.perf_counter()
            self.duration = (self.end_perf_counter - self.start_perf_counter) * 1000  # Convert to milliseconds
