import time
import socket
import getpass
from typing import List
from datetime import datetime
from pydantic import BaseModel
from dq.test import DQTest, Metric
from dq.core.config import DQConfig
from dq.connection import get_connection
from dq.validators import get_validator


class PerformanceCounter:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.duration = None

    def start(self):
        self.start_time = datetime.now()
        self._start_perf_counter = time.perf_counter()

    def stop(self):
        self.end_time = datetime.now()
        self._end_perf_counter = time.perf_counter()
        self.duration = (self._end_perf_counter - self._start_perf_counter) * 1000  # Convert to milliseconds

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_duration(self):
        return self.duration


class MetricResult(BaseModel):
    metric: Metric
    metric_value: float
    rag_status: str


class DQTestResult(BaseModel):
    environment: str
    host: str
    user: str
    test_status: str
    execution_status: str = "COMPLETED"
    exception: str
    test: DQTest
    metric_results: List[MetricResult]
    start_timestamp: datetime
    end_timestamp: datetime
    duration_ms: int


class DQTestRun(BaseModel):
    run_id: str
    start_timestamp: datetime
    end_timestamp: datetime
    duration_ms: int
    test_results: List[DQTestResult]


class DQTestProcessor:
    def __init__(self, config: DQConfig):
        self.config: DQConfig = config

    def _process_test(self, test: DQTest):
        counter = PerformanceCounter()
        counter.start()

        try:
            env = self.config.get_environment_by_name(test.environment)

            conn = get_connection(env)
            result = conn.select(test.test_query)

            metric_results = []
            test_status = 'GREEN'

            for metric in test.metrics:
                metric_value = result[metric.metric_variable][0]
                validator = get_validator(metric.rag)
                validation_result = validator.validate_metric(metric_value)
                metric_results.append(MetricResult(metric=metric,
                                                   metric_value=metric_value,
                                                   rag_status=validation_result))
                if validation_result == 'RED':
                    test_status = 'RED'
                elif validation_result == 'AMBER' and test_status != 'RED':
                    test_status = 'AMBER'

            counter.stop()

            test_result = DQTestResult(
                environment=test.environment,
                host=socket.gethostname(),
                user=getpass.getuser(),
                execution_status="COMPLETED",
                test_status=test_status,
                exception="",
                test=test,
                metric_results=metric_results,
                start_timestamp=counter.get_start_time(),
                end_timestamp=counter.get_end_time(),
                duration_ms=counter.get_duration()
            )
            return test_result

        except Exception as e:
            counter.stop()
            return DQTestResult(
                environment=test.environment,
                host=socket.gethostname(),
                user=getpass.getuser(),
                test_status="UNKNOWN",
                execution_status="FAILED",
                exception=str(e),
                test=test,
                metric_results=[],
                start_timestamp=counter.get_start_time(),
                end_timestamp=counter.get_end_time(),
                duration_ms=counter.get_duration()
            )

    def process(self, tests: List[DQTest]) -> DQTestRun:
        counter = PerformanceCounter()
        counter.start()

        results = []
        for test in tests:
            res = self._process_test(test)
            results.append(res)

        counter.stop()

        return DQTestRun(run_id="100",
                         start_timestamp=counter.get_start_time(),
                         end_timestamp=counter.get_end_time(),
                         duration_ms=counter.get_duration(),
                         test_results=results
                         )
