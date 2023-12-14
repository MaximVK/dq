
import time 
import socket
import getpass
from typing import List
from datetime import datetime, timedelta
from pydantic import BaseModel
from dq.test import DQTest, Metric
from dq.config import Configuration
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


class TestProcessor:
    def __init__(self, config: Configuration):
        self.config: Configuration = config

    def process(self, tests: List[DQTest]):
        for test in tests:
            start_time = time.perf_counter()

            try:
                env = self.config.get_environment_by_name(test.environment)

                with get_connection(env) as conn:
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
                    test_status=test_status,
                    exception="",
                    test=test,
                    metric_results=metric_results,
                    start_timestamp=start_dt,
                    end_timestamp=end_dt,
                    duration=duration_ms
                )
                yield test_result

            except Exception as e:
                yield DQTestResult(
                    environment=test.environment,
                    host=socket.gethostname(),
                    user=getpass.getuser(),
                    test_status="UNKNOWN",
                    execution_status = "FAILED",
                    exception=str(e),
                    test=test,
                    metric_results=[],
                    start_timestamp=datetime.now(),
                    end_timestamp=datetime.now(),
                    duration=0.0
                )