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



class PerformanceTimer:
    class TimerResult:
        def __init__(self, start_time: datetime, start_perf_counter: float):
            self.end_time = datetime.now()
            self.end_perf_counter = time.perf_counter()
            self.start_time = start_time
            self.duration = int((self.end_perf_counter - start_perf_counter) * 1000)  # Convert to milliseconds

    class TimerSession:
        def __init__(self):
            self.start_time = datetime.now()
            self.start_perf_counter = time.perf_counter()

        def stop(self) -> 'PerformanceTimer.TimerResult':
            return PerformanceTimer.TimerResult(self.start_time, self.start_perf_counter)

    @staticmethod
    def start() -> TimerSession:
        return PerformanceTimer.TimerSession()


timer = PerformanceTimer.start()
print(timer.start_time)
# logic here
timer_result = timer.stop()

print(timer_result.start_time)
print(timer_result.end_time)
print(timer_result.duration)







