import time
from datetime import datetime



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

    def stop(self) -> TimerResult:
        return TimerResult(self.start_time, self.start_perf_counter)

def start() -> TimerSession:
    return TimerSession()





