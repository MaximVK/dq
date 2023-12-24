import socket
import getpass
from typing import List
from datetime import datetime
from pydantic import BaseModel
from dq.test import DQTest, Metric
from dq.core.config import DQConfig
from dq.connection import get_connection
import dq.utils.performance_timer as pefr_timer
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
        timer = pefr_timer.start()

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

            timer_result = timer.stop()

            test_result = DQTestResult(
                environment=test.environment,
                host=socket.gethostname(),
                user=getpass.getuser(),
                execution_status="COMPLETED",
                test_status=test_status,
                exception="",
                test=test,
                metric_results=metric_results,
                start_timestamp=timer_result.start_time,
                end_timestamp=timer_result.end_time,
                duration_ms=timer_result.duration
            )

        except Exception as e:
            timer_result = timer.stop()

            test_result = DQTestResult(
                environment=test.environment,
                host=socket.gethostname(),
                user=getpass.getuser(),
                test_status="UNKNOWN",
                execution_status="FAILED",
                exception=str(e),
                test=test,
                metric_results=[],
                start_timestamp=timer_result.start_time,
                end_timestamp=timer_result.end_time,
                duration_ms=timer_result.duration
            )
        return test_result

    def process(self, tests: List[DQTest]) -> DQTestRun:
        timer = pefr_timer.start()

        results = []
        for test in tests:
            res = self._process_test(test)
            results.append(res)

        timer_result = timer.stop()

        return DQTestRun(run_id="100",
                         start_timestamp=timer_result.start_time,
                         end_timestamp=timer_result.end_time,
                         duration_ms=timer_result.duration,
                         test_results=results
                         )
