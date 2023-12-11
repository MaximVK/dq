from dataclasses import dataclass
from typing import List
from datetime import datetime
from enum import Enum
from typing import List, Optional


class Severity(Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    CRITICAL = 'Critical'

    def __str__(self):
        return self.valuev

@dataclass
class Metric:
    metric_variable: str  # Identifier for the metric
    description: str      # Description of the metric
    validate_condition: str  # Condition to validate the metric
    labels: List[str]     # Labels associated with the metric

@dataclass
class DQTest:
    dataset_grou: str     # Dataset group to run the test on
    dataset: str          # Dataset to run the test on
    test_name: str        # Name of the data quality test
    environment: str      # Environment where the test is run
    labels: List[str]     # Labels associated with the test
    metrics: List[Metric] # Metrics used in the test
    severity: Severity         # Severity level of the test
    test_query: str       # Query to execute the test
    details_query: str    # Query to get detailed results of the test

@dataclass
class MetricResult:
    metric: Metric       # The metric being measured
    metric_value: float  # The value of the metric
    rag_status: str      # RAG (Red, Amber, Green) status of the metric


@dataclass
class DQTestResult:
    environment:str            # This is the environment where the test is run
    host:str                   # Represents the hostname or IP address of the system
    user:str                   # Represents the username associated with the host
    status:str                 # Represents the status of the test execution
    exception:str              # Represents any exception or error message encountered during the test
    test:DQTest                # Represents an instance of the DQTest class
    metric_results:List[MetricResult]  # Represents a list of MetricResult objects which contain the results of individual metrics
    start_timestamp:datetime   # Represents the timestamp when the test execution started
    end_timestamp:datetime     # Represents the timestamp when the test execution ended
    duration:float             # Represents the duration or time taken to execute the test in seconds







