import time
import socket
import getpass
from typing import List
from datetime import datetime, timedelta
from pydantic import BaseModel
from dq.test import DQTest, Metric
from dq.core.config import DQConfig
from dq.connection import get_connection
from dq.validators import get_validator


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
        start_time = time.perf_counter()

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

            end_time = time.perf_counter()
            duration = end_time - start_time

            start_dt = datetime.now()
            end_dt = start_dt + timedelta(seconds=duration)
            duration_ms = int(duration * 1000)

            test_result = DQTestResult(
                environment=test.environment,
                host=socket.gethostname(),
                user=getpass.getuser(),
                execution_status="COMPLETED",
                test_status=test_status,
                exception="",
                test=test,
                metric_results=metric_results,
                start_timestamp=start_dt,
                end_timestamp=end_dt,
                duration_ms=duration_ms
            )
            return test_result

        except Exception as e:
            return DQTestResult(
                environment=test.environment,
                host=socket.gethostname(),
                user=getpass.getuser(),
                test_status="UNKNOWN",
                execution_status="FAILED",
                exception=str(e),
                test=test,
                metric_results=[],
                start_timestamp=datetime.now(),
                end_timestamp=datetime.now(),
                duration_ms=0.0
            )

    def process(self, tests: List[DQTest]) -> DQTestRun:
        start_time = time.perf_counter()
        results = []
        for test in tests:
            res = self._process_test(test)
            results.append(res)

        end_time = time.perf_counter()
        duration = end_time - start_time
        start_dt = datetime.now()
        end_dt = start_dt + timedelta(seconds=duration)
        duration_ms = int(duration * 1000)

        return DQTestRun(run_id="100",
                         start_timestamp=start_time,
                         end_timestamp=end_time,
                         duration_ms=duration_ms,
                         test_results=results
                         )
