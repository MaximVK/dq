import pytest
from dq.utils.performance_timer import TimerResult, TimerSession, start
from datetime import datetime

def test_timerresult():
    start_time = datetime.now()
    start_perf_counter = 123.456
    result = TimerResult(start_time, start_perf_counter)
    assert isinstance(result, TimerResult)
    assert result.start_time == start_time
    assert isinstance(result.duration, int)


def test_timersession():
    session = TimerSession()
    assert isinstance(session, TimerSession)
    result = session.stop()
    assert isinstance(result, TimerResult)


def test_start():
    session = start()
    assert isinstance(session, TimerSession)